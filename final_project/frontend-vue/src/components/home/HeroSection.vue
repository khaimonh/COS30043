<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useI18n } from "../../i18n";
import Mark from "../ui/Mark.vue";

const { t, tf } = useI18n();

const tick = ref(0);
let timer: ReturnType<typeof setInterval> | undefined;

onMounted(() => {
  timer = setInterval(() => {
    tick.value += 1;
  }, 12);
});
onUnmounted(() => clearInterval(timer));

const quota = 500;
const count = computed(() => Math.min(tick.value * 5, quota));

const current = ref({
  symbol: "VNINDEX",
  price: "1,324.62",
  chg: "+14.32",
  arrow: "▲",
});

const quotes = [
  { symbol: "VN30", price: "1,368.4", chg: "+1.1%", dir: "up" },
  { symbol: "VNM", price: "78.6", chg: "+0.9%", dir: "up" },
  { symbol: "VIC", price: "46.3", chg: "−0.6%", dir: "down" },
  { symbol: "FPT", price: "112.8", chg: "+2.1%", dir: "up" },
  { symbol: "HPG", price: "29.9", chg: "+1.5%", dir: "up" },
  { symbol: "TCB", price: "39.4", chg: "−0.3%", dir: "down" },
] as const;

const specs = [
  { key: "home.spec.origin", value: "HCMC" },
  { key: "home.spec.liquidity", value: "2,463 symbols" },
  { key: "home.spec.sessions", value: "30 min" },
  { key: "home.spec.feed", value: "2 min" },
  { key: "home.spec.est", value: "2001" },
] as const;
</script>

<template>
  <section class="relative">
    <div class="mx-auto grid max-w-6xl gap-10 px-4 pt-16 pb-10 sm:px-6 sm:pt-20 lg:grid-cols-12 lg:gap-8 lg:pt-24">
      <div class="lg:col-span-7">
        <div class="flex items-center gap-4">
          <Mark />
          <span class="font-mono text-xs tracking-[0.25em] text-muted">{{ t("brand.name").toUpperCase() }} · FOLIO</span>
        </div>

        <div class="mt-8 flex items-end gap-3 font-display text-[clamp(3.5rem,12vw,7.5rem)] font-bold leading-[0.9] tracking-[-0.03em] text-ink">
          <span class="tabular-nums">{{ count }}</span>
          <span class="text-4xl leading-none text-muted sm:text-6xl">+</span>
        </div>

        <p class="mt-4 max-w-[56ch] font-mono text-sm leading-relaxed tracking-wide text-muted">
          {{ t("home.hero") }}
        </p>

        <p class="mt-6 max-w-[64ch] text-lg text-ink">
          {{ t("home.lede") }}
        </p>

        <div class="mt-8 flex flex-wrap items-center gap-3 font-mono text-xs tracking-[0.15em] text-muted">
          <span>{{ tf("home.liveQuote", current) }}</span>
          <span class="text-rule">/</span>
          <span>{{ tf("home.liveArrow", current) }}</span>
        </div>

        <div class="mt-8 flex flex-wrap gap-2">
          <span
            v-for="q in quotes"
            :key="q.symbol"
            class="rounded-full border border-rule px-3 py-1 font-mono text-xs"
          >
            <span class="text-ink">{{ q.symbol }}</span>
            <span class="mx-1.5 text-muted">{{ q.price }}</span>
            <span :class="q.dir === 'up' ? 'text-up' : 'text-down'">{{ q.chg }}</span>
          </span>
        </div>
      </div>

      <div class="lg:col-span-5">
        <div class="rounded-2xl border border-rule bg-paper-2 p-6">
          <p class="font-mono text-xs tracking-[0.25em] text-muted">{{ t("home.spec.title").toUpperCase() }}</p>
          <p class="mt-1 font-mono text-[10px] tracking-[0.15em] text-muted/70">{{ t("home.spec.demoNote") }}</p>
          <dl class="mt-4 space-y-3 font-mono text-sm">
            <div v-for="s in specs" :key="s.key" class="flex justify-between border-b border-rule pb-3 last:border-0 last:pb-0">
              <dt class="text-muted">{{ t(s.key) }}</dt>
              <dd class="text-ink">{{ s.value }}</dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  </section>
</template>
