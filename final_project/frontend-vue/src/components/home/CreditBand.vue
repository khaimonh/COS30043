<script setup lang="ts">
import { useI18n } from "../../i18n";

const { t } = useI18n();

const rows = [
  { key: "home.credit.memo", value: "12", tag: "A1" },
  { key: "home.credit.positions", value: "40", tag: "B2" },
  { key: "home.credit.funds", value: "120,000", tag: "C3" },
  { key: "home.credit.orders", value: "500", tag: "D4" },
] as const;
</script>

<template>
  <section class="border-t-4 border-band bg-paper">
    <div class="mx-auto grid max-w-6xl gap-8 px-4 py-14 sm:px-6 lg:grid-cols-2">
      <div class="lg:pr-8">
        <p class="font-mono text-xs tracking-[0.25em] text-muted">{{ t("home.credit.title").toUpperCase() }}</p>
        <p class="mt-4 max-w-[40ch] text-lg text-ink">{{ t("home.credit.statement") }}</p>
      </div>

      <div class="pl-6 lg:pl-10">
        <dl class="space-y-4 font-mono text-sm">
          <div
            v-for="r in rows"
            :key="r.key"
            class="flex items-baseline justify-between gap-4 border-b border-rule pb-4 last:border-0 last:pb-0"
          >
            <dt class="flex items-center gap-2.5">
              <span class="rounded-full bg-band px-2 py-0.5 text-[10px] tracking-widest text-band-ink">{{ r.tag }}</span>
              <span class="text-muted">{{ t(r.key) }}</span>
            </dt>
            <dd class="text-ink">{{ r.value }}</dd>
          </div>
        </dl>
      </div>
    </div>
  </section>
</template>
