<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { useI18n } from "../../i18n";
import ButtonLink from "../ui/ButtonLink.vue";

const { t } = useI18n();
const count = ref(0);

let raf = 0;
const TARGET = 500;
const DURATION = 400;

onMounted(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const start = performance.now();
  const step = (now: number) => {
    const p = reduce ? 1 : Math.min(1, (now - start) / DURATION);
    const eased = 1 - Math.pow(1 - p, 3);
    count.value = Math.round(eased * TARGET);
    if (p < 1) raf = requestAnimationFrame(step);
  };
  raf = requestAnimationFrame(step);
});

onBeforeUnmount(() => cancelAnimationFrame(raf));
</script>

<template>
  <section class="mx-auto w-full max-w-6xl px-4 pb-16 pt-10 sm:px-6 sm:pb-24 sm:pt-14">
    <div class="grid items-center gap-12 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,0.9fr)] lg:gap-16">
      <div>
        <p class="font-mono text-xs uppercase tracking-[0.14em] text-accent-hover">
          {{ t("home.heroTag") }}
        </p>
        <p class="mt-6 font-display text-[clamp(4rem,16vw,10.5rem)] font-semibold leading-[0.9] tracking-[-0.04em] tabular-nums">
          <span aria-hidden="true">{{ count.toLocaleString("en-US") }}</span>
          <span class="sr-only">{{ t("home.heroFigure") }}</span>
          <span class="ml-3 align-top font-mono text-[0.32em] font-medium tracking-normal text-muted">
            {{ t("home.stat2Label") }}
          </span>
        </p>
        <h1 class="mt-8 max-w-[22ch] text-[clamp(2.5rem,5vw,4.25rem)] font-semibold leading-[1.02] tracking-[-0.03em]">
          {{ t("home.title") }}
        </h1>
        <p class="mt-6 max-w-[65ch] text-base leading-relaxed text-muted sm:text-lg">
          {{ t("home.welcome") }}
        </p>
        <div class="mt-10 flex flex-wrap items-center gap-4">
          <ButtonLink to="/news" size="lg">
            {{ t("home.ctaPrimary") }}
          </ButtonLink>
          <ButtonLink to="/about" size="lg" variant="outline">
            {{ t("home.ctaSecondary") }}
          </ButtonLink>
        </div>
      </div>

      <div class="relative">
        <div class="absolute -inset-6 rounded-3xl bg-accent-soft blur-3xl" aria-hidden="true" />
        <img
          src="/images/hero-chart.svg"
          :alt="t('home.image1Alt')"
          class="relative w-full rounded-2xl border border-border bg-surface"
        />
      </div>
    </div>
  </section>
</template>
