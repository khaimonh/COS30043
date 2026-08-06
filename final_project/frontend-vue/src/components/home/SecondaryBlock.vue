<script setup lang="ts">
import { useI18n } from "../../i18n";

const { t, tf } = useI18n();

const sectors = [
  { key: "home.sector.banks", value: "≈ 26%", dir: "up" },
  { key: "home.sector.realty", value: "≈ 14%", dir: "up" },
  { key: "home.sector.materials", value: "≈ 12%", dir: "down" },
  { key: "home.sector.cons", value: "≈ 11%", dir: "up" },
] as const;
</script>

<template>
  <section class="border-t border-rule bg-paper-2">
    <div class="mx-auto grid max-w-6xl gap-10 px-4 py-16 sm:px-6 sm:py-20 lg:grid-cols-2">
      <div>
        <p class="font-mono text-xs tracking-[0.25em] text-muted">{{ t("home.sector.title").toUpperCase() }}</p>
        <p class="mt-6 max-w-[58ch] text-[clamp(1.5rem,4vw,2.5rem)] font-display font-bold leading-[1.1] tracking-[-0.02em]">
          {{ t("home.sector.statement") }}
        </p>
        <div class="mt-8 space-y-3 font-mono text-sm">
          <div v-for="s in sectors" :key="s.key" class="flex items-center justify-between gap-4 border-b border-rule pb-3 last:border-0">
            <dt class="text-muted">{{ t(s.key) }}</dt>
            <dd class="flex items-baseline gap-2">
              <span class="text-ink">{{ s.value }}</span>
              <span :class="s.dir === 'up' ? 'text-up' : 'text-down'">{{ s.dir === "up" ? "▲" : "▼" }}</span>
            </dd>
          </div>
        </div>
      </div>

      <figure>
        <div class="rounded-2xl border border-rule bg-paper p-4">
          <img
            src="/images/hero-chart.svg"
            alt="VN-INDEX daily candles"
            class="w-full"
            width="720"
            height="440"
          />
          <figcaption class="mt-3 flex items-center justify-between font-mono text-[11px] tracking-[0.15em] text-muted">
            <span>{{ t("home.chart.caption").toUpperCase() }}</span>
            <span>{{ tf("home.chart.source", { source: "Fluxus" }) }}</span>
          </figcaption>
        </div>
      </figure>
    </div>
  </section>
</template>
