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
          <div class="flex items-baseline justify-between gap-3">
            <p class="font-mono text-xs tracking-[0.25em] text-muted">
              {{ t("footer.specTitle").toUpperCase() }}
            </p>
            <p class="font-mono text-[10px] tracking-[0.2em] text-muted/70">
              {{ t("footer.demoNote") }}
            </p>
          </div>
          <dl class="mt-4 space-y-3 font-mono text-sm">
            <div
              v-for="row in specs"
              :key="row.key"
              class="flex items-baseline justify-between gap-4 border-b border-rule pb-3 last:border-0 last:pb-0"
            >
              <dt class="text-muted">{{ t(row.key) }}</dt>
              <dd class="text-right text-ink">{{ row.value }}</dd>
            </div>
          </dl>
        </div>

        <ImagePicker />

        <div class="rounded-2xl border border-rule p-6">
          <p class="mb-4 font-mono text-xs tracking-[0.25em] text-muted">{{ t("about.visitTitle").toUpperCase() }}</p>
          <GreetingForm />
        </div>
      </div>
    </div>
  </section>
</template>
