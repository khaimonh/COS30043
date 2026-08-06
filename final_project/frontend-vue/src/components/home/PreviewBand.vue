<script setup lang="ts">
import { useI18n } from "../../i18n";
import ButtonLink from "../ui/ButtonLink.vue";

const { t } = useI18n();
</script>

<template>
  <section class="mx-auto w-full max-w-6xl px-4 pb-20 sm:px-6 sm:pb-24">
    <div class="grid items-center gap-10 lg:grid-cols-2 lg:gap-14">
      <img
        src="/images/dashboard-preview.svg"
        :alt="t('home.image2Alt')"
        class="w-full rounded-2xl border border-border bg-surface"
      />
      <div>
        <h2 class="max-w-[22ch] text-3xl font-semibold tracking-tight sm:text-4xl">
          {{ t("home.ctaStripTitle") }}
        </h2>
        <p class="mt-4 max-w-[45ch] leading-relaxed text-muted">
          {{ t("home.ctaStripNote") }}
        </p>
        <ButtonLink to="/news" size="lg" class="mt-9">
          {{ t("home.ctaPrimary") }}
        </ButtonLink>
      </div>
    </div>
  </section>
</template>
