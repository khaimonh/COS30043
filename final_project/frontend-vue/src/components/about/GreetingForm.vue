<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "../../i18n";
import Button from "../ui/Button.vue";
import Input from "../ui/Input.vue";

const { t, tf } = useI18n();
const firstName = ref("");
const lastName = ref("");
const name = ref<string | null>(null);

function onSubmit(): void {
  const full = `${firstName.value} ${lastName.value}`.trim();
  name.value = full.length > 0 ? full : null;
}
</script>

<template>
  <form class="space-y-5" noValidate @submit.prevent="onSubmit">
    <div class="grid gap-4 sm:grid-cols-2">
      <label class="block">
        <span class="mb-1.5 block text-sm font-medium text-ink">
          {{ t("about.firstNameLabel") }}
        </span>
        <Input
          v-model="firstName"
          :placeholder="t('about.firstNamePlaceholder')"
          auto-complete="given-name"
          name="firstName"
        />
      </label>
      <label class="block">
        <span class="mb-1.5 block text-sm font-medium text-ink">
          {{ t("about.lastNameLabel") }}
        </span>
        <Input
          v-model="lastName"
          :placeholder="t('about.lastNamePlaceholder')"
          auto-complete="family-name"
          name="lastName"
        />
      </label>
    </div>
    <Button type="submit">{{ t("about.greetButton") }}</Button>
    <p v-if="name !== null" class="text-lg font-semibold tracking-tight text-up">
      {{ tf("about.welcome", { name }) }}
    </p>
  </form>
</template>
