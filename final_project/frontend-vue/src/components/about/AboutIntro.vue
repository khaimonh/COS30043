<script setup lang="ts">
import { useI18n } from "../../i18n";
import GreetingForm from "./GreetingForm.vue";
import ImagePicker from "./ImagePicker.vue";

const { t } = useI18n();

const specs = [
  { key: "footer.spec.exchanges", value: "HOSE · HNX · UPCOM" },
  { key: "footer.spec.coverage", value: "500+ securities" },
  { key: "footer.spec.engine", value: "FIFO · RabbitMQ" },
  { key: "footer.spec.settlement", value: "VND · T+2" },
  { key: "footer.spec.calendar", value: "Mon–Fri · 09:00–15:00" },
] as const;
</script>

<template>
  <section class="border-top border-rule bg-paper">
    <div class="mx-auto max-w-6xl row g-5 px-3 py-5 px-sm-4 py-sm-5">
      <div class="col-12 col-lg-7">
        <p class="font-mono text-xs tracking-[0.25em] text-muted">{{ t("about.kicker").toUpperCase() }}</p>
        <h1 class="mt-3 max-w-[20ch] font-display text-[clamp(2.5rem,7vw,5rem)] fw-bold leading-[1.02] tracking-[-0.03em]">
          {{ t("about.title") }}
        </h1>
        <p class="mt-5 max-w-[62ch] text-lg leading-relaxed text-ink">{{ t("about.lede") }}</p>
        <p class="mt-3 max-w-[62ch] leading-relaxed text-muted">{{ t("about.origin") }}</p>
      </div>

      <div class="d-flex flex-column gap-5 col-12 col-lg-5">
        <div class="rounded-4 border border-rule bg-paper-2 p-4">
          <div class="d-flex align-items-baseline justify-content-between gap-3">
            <p class="font-mono text-xs tracking-[0.25em] text-muted">
              {{ t("footer.specTitle").toUpperCase() }}
            </p>
            <p class="font-mono text-[10px] tracking-[0.2em] text-muted/70">
              {{ t("footer.demoNote") }}
            </p>
          </div>
          <dl class="mt-3 d-flex flex-column gap-3 font-mono text-sm">
            <div
              v-for="row in specs"
              :key="row.key"
              class="d-flex align-items-baseline justify-content-between gap-4 border-bottom border-rule pb-3 last:border-0 last:pb-0"
            >
              <dt class="text-muted">{{ t(row.key) }}</dt>
              <dd class="text-end text-ink">{{ row.value }}</dd>
            </div>
          </dl>
        </div>

        <ImagePicker />

        <div class="rounded-4 border border-rule p-4">
          <p class="mb-3 font-mono text-xs tracking-[0.25em] text-muted">{{ t("about.visitTitle").toUpperCase() }}</p>
          <GreetingForm />
        </div>
      </div>
    </div>
  </section>
</template>
