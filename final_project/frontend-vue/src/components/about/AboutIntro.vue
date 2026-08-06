<script setup lang="ts">
import { useI18n } from "../../i18n";
import GreetingForm from "./GreetingForm.vue";

const { t } = useI18n();

const facts = [
  { key: "about.fact.founded", value: "2001" },
  { key: "about.fact.employees", value: "89" },
  { key: "about.fact.asset", value: "₫ 12.4 bn" },
  { key: "about.fact.cto", value: "Hà Nội" },
] as const;
</script>

<template>
  <section class="border-t border-rule bg-paper">
    <div class="mx-auto grid max-w-6xl gap-10 px-4 py-16 sm:px-6 sm:py-20 lg:grid-cols-12 lg:gap-12">
      <div class="lg:col-span-7">
        <p class="font-mono text-xs tracking-[0.25em] text-muted">{{ t("about.kicker").toUpperCase() }}</p>
        <h1 class="mt-4 max-w-[20ch] font-display text-[clamp(2.5rem,7vw,5rem)] font-bold leading-[1.02] tracking-[-0.03em]">
          {{ t("about.title") }}
        </h1>
        <p class="mt-8 max-w-[62ch] text-lg leading-relaxed text-ink">{{ t("about.lede") }}</p>
        <p class="mt-5 max-w-[62ch] leading-relaxed text-muted">{{ t("about.origin") }}</p>
      </div>

      <div class="flex flex-col gap-5 lg:col-span-5">
        <div class="rounded-2xl border border-rule bg-paper-2 p-6">
          <p class="font-mono text-xs tracking-[0.25em] text-muted">{{ t("about.factsTitle").toUpperCase() }}</p>
          <p class="mt-1 font-mono text-[10px] tracking-[0.15em] text-muted/70">{{ t("about.demoNote") }}</p>
          <dl class="mt-4 space-y-3 font-mono text-sm">
            <div v-for="f in facts" :key="f.key" class="flex justify-between border-b border-rule pb-3 last:border-0 last:pb-0">
              <dt class="text-muted">{{ t(f.key) }}</dt>
              <dd class="text-ink">{{ f.value }}</dd>
            </div>
          </dl>
        </div>

        <figure>
          <div class="grid grid-cols-2 gap-3">
            <img src="/images/ocean.svg" alt="Ocean scene" class="rounded-2xl border border-rule" width="420" height="280" />
            <img src="/images/mountain.svg" alt="Mountain scene" class="rounded-2xl border border-rule" width="420" height="280" />
          </div>
        </figure>

        <div class="rounded-2xl border border-rule p-6">
          <p class="mb-4 font-mono text-xs tracking-[0.25em] text-muted">{{ t("about.visitTitle").toUpperCase() }}</p>
          <GreetingForm />
        </div>
      </div>
    </div>
  </section>
</template>
