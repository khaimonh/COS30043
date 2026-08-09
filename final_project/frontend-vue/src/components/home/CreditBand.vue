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
  <section class="border-top border-4 border-band bg-paper">
    <div class="mx-auto max-w-6xl row row-cols-1 row-cols-lg-2 g-5 px-3 py-4 px-sm-4">
      <div class="pe-lg-5">
        <p class="font-mono text-xs tracking-[0.25em] text-muted">{{ t("home.credit.title").toUpperCase() }}</p>
        <p class="mt-3 max-w-[40ch] text-lg text-ink">{{ t("home.credit.statement") }}</p>
      </div>

      <div class="ps-4 ps-lg-5">
        <dl class="d-flex flex-column gap-4 font-mono text-sm">
          <div
            v-for="r in rows"
            :key="r.key"
            class="d-flex align-items-baseline justify-content-between gap-4 border-bottom border-rule pb-3 last:border-0 last:pb-0"
          >
            <dt class="d-flex align-items-center gap-2.5">
              <span class="rounded-pill bg-band px-2 py-0.5 text-[10px] tracking-widest text-band-ink">{{ r.tag }}</span>
              <span class="text-muted">{{ t(r.key) }}</span>
            </dt>
            <dd class="text-ink">{{ r.value }}</dd>
          </div>
        </dl>
      </div>
    </div>
  </section>
</template>
