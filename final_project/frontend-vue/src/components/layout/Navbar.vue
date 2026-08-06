<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import { useI18n } from "../../i18n";
import ButtonLink from "../ui/ButtonLink.vue";
import LangToggle from "./LangToggle.vue";

const { t } = useI18n();
const route = useRoute();
const open = ref(false);

const links = [
  { href: "/", key: "nav.home" },
  { href: "/about", key: "nav.about" },
  { href: "/news", key: "nav.news" },
] as const;

function isActive(href: string): boolean {
  return href === "/" ? route.path === "/" : route.path.startsWith(href);
}
</script>

<template>
  <header class="fixed inset-x-0 top-4 z-[300] flex justify-center px-4">
    <div class="flex max-w-[720px] items-center gap-1 rounded-full border border-border bg-background/75 py-1.5 pl-2.5 pr-1.5 shadow-float backdrop-blur-xl">
      <RouterLink to="/" class="flex items-center gap-2.5">
        <span class="grid h-7 w-7 place-items-center rounded-full bg-accent">
          <svg viewBox="0 0 24 24" class="h-4 w-4 text-white" aria-hidden="true">
            <rect x="4" y="9" width="3" height="9" rx="0.5" fill="currentColor" />
            <rect x="10.5" y="4" width="3" height="14" rx="0.5" fill="currentColor" />
            <rect x="17" y="7" width="3" height="11" rx="0.5" fill="currentColor" />
          </svg>
        </span>
        <span class="font-mono text-base font-medium tracking-tight text-foreground">
          Fluxus
        </span>
      </RouterLink>

      <nav class="hidden items-center gap-0.5 lg:flex" aria-label="Main">
        <RouterLink
          v-for="link in links"
          :key="link.href"
          :to="link.href"
          :class="[
            'rounded-full px-3 py-1.5 text-sm font-medium transition-colors duration-150',
            isActive(link.href) ? 'bg-surface-2 text-foreground' : 'text-muted hover:text-foreground',
          ]"
        >
          {{ t(link.key) }}
        </RouterLink>
      </nav>

      <div class="flex items-center gap-1.5 pl-1">
        <LangToggle />
        <ButtonLink to="/news" size="sm" class="hidden lg:inline-flex">
          {{ t("nav.explore") }}
        </ButtonLink>
        <button
          type="button"
          class="grid h-9 w-9 place-items-center rounded-full text-muted transition-colors duration-150 hover:text-foreground lg:hidden"
          :aria-expanded="open"
          aria-label="Toggle menu"
          @click="open = !open"
        >
          <svg v-if="open" viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M6 6l12 12M18 6L6 18" stroke-linecap="round" />
          </svg>
          <svg v-else viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M4 7h16M4 12h16M4 17h16" stroke-linecap="round" />
          </svg>
        </button>
      </div>
    </div>

    <nav
      v-if="open"
      class="absolute top-full mt-2 w-full max-w-[220px] rounded-2xl border border-border bg-background/90 p-2 shadow-float backdrop-blur-xl lg:hidden"
      aria-label="Mobile"
    >
      <RouterLink
        v-for="link in links"
        :key="link.href"
        :to="link.href"
        class="block rounded-full px-3 py-2.5 text-sm font-medium transition-colors duration-150"
        :class="isActive(link.href) ? 'bg-surface-2 text-foreground' : 'text-muted hover:text-foreground'"
        @click="open = false"
      >
        {{ t(link.key) }}
      </RouterLink>
    </nav>
  </header>
</template>
