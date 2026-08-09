<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "../i18n";
import Button from "../components/ui/Button.vue";
import Input from "../components/ui/Input.vue";
import { login } from "../lib/session";
import { api } from "../lib/api";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const mode = ref<"login" | "register">("login");
const email = ref("");
const password = ref("");
const firstName = ref("");
const lastName = ref("");
const busy = ref(false);
const error = ref("");

async function submit() {
  busy.value = true;
  error.value = "";
  try {
    if (mode.value === "login") {
      await login(email.value, password.value);
    } else {
      await api("/auth/", {
        body: { first_name: firstName.value, last_name: lastName.value, email: email.value, password: password.value },
      });
      await login(email.value, password.value);
    }
    const redirect = (route.query.redirect as string) || "/market";
    router.replace(redirect);
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  } finally {
    busy.value = false;
  }
}
</script>

<template>
  <div class="mx-auto w-100 max-w-md px-3 pb-5 pt-5 px-sm-4 pt-sm-5">
    <p class="font-mono text-xs text-uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
    <h1 class="mt-3 font-display text-3xl fw-bold tracking-[-0.02em] text-ink sm:text-4xl">
      {{ mode === "login" ? t("auth.loginTitle") : t("auth.registerTitle") }}
    </h1>

    <form class="mt-5 d-flex flex-column gap-4 rounded-4 border border-rule bg-paper-2 p-4" @submit.prevent="submit">
      <label v-if="mode === 'register'" class="d-flex flex-column gap-1.5">
        <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("auth.firstName") }}</span>
        <Input v-model="firstName" required autocomplete="given-name" />
      </label>
      <label v-if="mode === 'register'" class="d-flex flex-column gap-1.5">
        <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("auth.lastName") }}</span>
        <Input v-model="lastName" required autocomplete="family-name" />
      </label>
      <label class="d-flex flex-column gap-1.5">
        <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("auth.email") }}</span>
        <Input v-model="email" type="email" required autocomplete="email" />
      </label>
      <label class="d-flex flex-column gap-1.5">
        <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("auth.password") }}</span>
        <Input v-model="password" type="password" required autocomplete="current-password" />
      </label>

      <p v-if="error" class="font-mono text-sm text-down">{{ error }}</p>

      <Button :disabled="busy" class="w-100">
        {{ mode === "login" ? t("auth.loginButton") : t("auth.registerButton") }}
      </Button>
    </form>

    <button
      type="button"
      class="mt-4 font-mono text-sm text-muted underline-offset-4 hover:text-ink hover:underline"
      @click="mode = mode === 'login' ? 'register' : 'login'"
    >
      {{ mode === "login" ? t("auth.registerCta") : t("auth.loginCta") }}
    </button>
  </div>
</template>
