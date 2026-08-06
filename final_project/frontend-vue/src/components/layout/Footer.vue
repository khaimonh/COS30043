<script setup lang="ts">
import { useI18n } from "../../i18n";

const { t, tf } = useI18n();

const links = [
  { href: "/", key: "nav.home" },
  { href: "/about", key: "nav.about" },
  { href: "/news", key: "nav.news" },
] as const;

const year = String(new Date().getFullYear());
</script>

<template>
  <footer class="border-t border-border">
    <div class="mx-auto w-full max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
      <p class="max-w-[28ch] text-[clamp(1.75rem,5vw,3.25rem)] font-semibold leading-[1.05] tracking-[-0.03em]">
        {{ t("footer.statement") }}
      </p>
      <div class="mt-10 flex flex-col gap-4 border-t border-border pt-5 text-sm sm:flex-row sm:items-baseline sm:justify-between">
        <span class="font-mono text-foreground">Fluxus</span>
        <nav class="flex flex-wrap gap-x-5 gap-y-2" aria-label="Footer">
          <RouterLink
            v-for="link in links"
            :key="link.href"
            :to="link.href"
            class="text-muted transition-colors duration-150 hover:text-foreground"
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
