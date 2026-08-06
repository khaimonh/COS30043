<script setup lang="ts">
import { useI18n, type Lang } from "../../i18n";

const { lang, setLang } = useI18n();

const options: { code: Lang; label: string }[] = [
  { code: "en", label: "EN" },
  { code: "vi", label: "VI" },
];
</script>

<template>
  <div
    class="inline-flex items-center rounded-full border border-border bg-surface p-0.5"
    role="group"
    aria-label="Language"
  >
    <button
      v-for="opt in options"
      :key="opt.code"
      type="button"
      :aria-pressed="lang === opt.code"
      :class="[
        'rounded-full px-3 py-1 font-mono text-xs font-medium transition-colors duration-150',
        lang === opt.code ? 'bg-accent text-white' : 'text-muted hover:text-foreground',
      ]"
      @click="setLang(opt.code)"
    >
      {{ opt.label }}
    </button>
  </div>
</template>
