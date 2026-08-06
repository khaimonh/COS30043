<script setup lang="ts">
import { useI18n } from "../i18n";
import GreetingForm from "../components/about/GreetingForm.vue";
import ImagePicker from "../components/about/ImagePicker.vue";

const { t } = useI18n();
</script>

<template>
  <div class="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
    <div class="max-w-[50ch]">
      <p class="font-display text-3xl font-semibold tracking-tight sm:text-4xl">
        {{ t("about.salutation") }}
      </p>
      <p class="mt-8 text-lg leading-relaxed text-muted">{{ t("about.paragraph") }}</p>
    </div>

    <div class="mt-16 max-w-[50ch]">
      <h2 class="text-xl font-semibold tracking-tight">{{ t("about.formTitle") }}</h2>
      <p class="mt-2 font-mono text-sm text-muted">{{ t("about.ps") }}</p>
      <div class="mt-8">
        <GreetingForm />
      </div>
    </div>

    <div class="mt-16 max-w-[50ch]">
      <h2 class="text-xl font-semibold tracking-tight">{{ t("about.sceneTitle") }}</h2>
      <p class="mt-2 font-mono text-sm text-muted">{{ t("about.welcomeHint") }}</p>
      <div class="mt-8">
        <ImagePicker />
      </div>
    </div>
  </div>
</template>
