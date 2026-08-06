<script setup lang="ts">
import { useI18n } from "../../i18n";

const { t } = useI18n();

const rows = [
  { name: "home.spec1Name", value: "home.spec1Value", note: "home.spec1Note" },
  { name: "home.spec2Name", value: "home.spec2Value", note: "home.spec2Note" },
  { name: "home.spec3Name", value: "home.spec3Value", note: "home.spec3Note" },
  { name: "home.spec4Name", value: "home.spec4Value", note: "home.spec4Note" },
] as const;
</script>

<template>
  <section class="mx-auto w-full max-w-6xl px-4 pb-16 sm:px-6 sm:pb-24">
    <h2 class="max-w-[22ch] text-3xl font-semibold tracking-tight sm:text-4xl">
      {{ t("home.specTitle") }}
    </h2>
    <div class="mt-10 divide-y divide-border border-y border-border">
      <div
        v-for="row in rows"
        :key="row.name"
        class="grid gap-2 py-5 sm:grid-cols-[1fr_auto] sm:items-baseline sm:gap-8"
      >
        <div>
          <h3 class="font-semibold tracking-tight">{{ t(row.name) }}</h3>
          <p class="mt-1 max-w-[65ch] text-sm leading-relaxed text-muted">
            {{ t(row.note) }}
          </p>
        </div>
        <p class="font-mono text-sm text-accent-hover sm:text-right">
          {{ t(row.value) }}
        </p>
      </div>
    </div>
  </section>
</template>
