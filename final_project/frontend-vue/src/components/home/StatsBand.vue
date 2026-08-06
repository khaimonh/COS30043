<script setup lang="ts">
import { useI18n } from "../../i18n";

const { t } = useI18n();

const stats = [
  { num: "home.stat1Num", label: "home.stat1Label" },
  { num: "home.stat2Num", label: "home.stat2Label" },
  { num: "home.stat3Num", label: "home.stat3Label" },
] as const;
</script>

<template>
  <section class="mx-auto w-full max-w-6xl px-4 pb-16 sm:px-6 sm:pb-24">
    <dl class="grid gap-8 sm:grid-cols-3">
      <div v-for="s in stats" :key="s.num" class="flex flex-col border-t border-border pt-5">
        <dd class="order-1 font-display text-5xl font-semibold tracking-tight tabular-nums">
          {{ t(s.num) }}
        </dd>
        <dt class="order-2 mt-2 font-mono text-xs uppercase tracking-[0.14em] text-muted">
          {{ t(s.label) }}
        </dt>
      </div>
    </dl>
  </section>
</template>
