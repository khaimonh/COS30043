<script setup lang="ts">
import { useI18n } from "../../i18n";
import Mark from "../ui/Mark.vue";

const { t, tf } = useI18n();

const links = [
  { href: "/", key: "nav.home" },
  { href: "/about", key: "nav.about" },
  { href: "/news", key: "nav.news" },
] as const;

const year = String(new Date().getFullYear());
</script>

<template>
  <footer class="border-t border-rule bg-paper">
    <div class="mx-auto w-full max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
      <p class="max-w-[28ch] text-[clamp(1.75rem,5vw,3.25rem)] font-display font-bold leading-[1.05] tracking-[-0.02em]">
        {{ t("footer.statement") }}
      </p>
      <div class="mt-12 flex flex-col gap-5 border-t border-rule pt-6 text-sm sm:flex-row sm:items-center sm:justify-between">
        <span class="flex items-center gap-3">
          <Mark size="sm" />
          <span class="font-mono text-ink">{{ t("brand.name") }}</span>
        </span>
        <nav class="flex flex-wrap gap-x-5 gap-y-2" aria-label="Footer">
          <RouterLink
            v-for="link in links"
            :key="link.href"
            :to="link.href"
            class="text-muted transition-colors duration-150 hover:text-ink"
          >
            {{ t(link.key) }}
          </RouterLink>
        </nav>
        <span class="font-mono text-xs text-muted">
          {{ tf("footer.rights", { year }) }}
        </span>
      </div>
    </div>
  </footer>
</template>
