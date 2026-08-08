<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useI18n } from "../i18n";
import Button from "../components/ui/Button.vue";
import Input from "../components/ui/Input.vue";
import { api } from "../lib/api";
import { fmtShortDate } from "../lib/format";
import type { BankAccount } from "../lib/types";

const { t } = useI18n();

const accounts = ref<BankAccount[]>([]);
const bankName = ref("");
const accountNumber = ref("");
const error = ref("");
const busy = ref(false);

async function load() {
  try {
    accounts.value = await api<BankAccount[]>("/bank-accounts");
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  }
}

async function link() {
  error.value = "";
  busy.value = true;
  try {
    await api("/bank-accounts", { body: { bank_name: bankName.value, account_number: accountNumber.value } });
    bankName.value = "";
    accountNumber.value = "";
    await load();
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  } finally {
    busy.value = false;
  }
}

async function unlink(a: BankAccount) {
  error.value = "";
  try {
    await api(`/bank-accounts/${a.bank_account_id}`, { method: "DELETE" });
    await load();
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  }
}

onMounted(load);
</script>

<template>
  <div class="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
    <header class="pb-10">
      <p class="font-mono text-xs uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
      <h1 class="mt-3 font-display text-3xl font-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("nav.bank") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("bank.subtitle") }}</p>
    </header>

    <p v-if="error" class="mb-4 font-mono text-sm text-down">{{ error }}</p>

    <form class="mb-8 flex flex-col gap-3 rounded-2xl border border-rule bg-paper-2 p-6 sm:flex-row sm:items-end" @submit.prevent="link">
      <label class="flex flex-col gap-1.5 sm:max-w-[14rem]">
        <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">{{ t("bank.name") }}</span>
        <Input v-model="bankName" required />
      </label>
      <label class="flex flex-col gap-1.5">
        <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">{{ t("bank.number") }}</span>
        <Input v-model="accountNumber" inputmode="numeric" required />
      </label>
      <Button :disabled="busy" class="sm:mb-0.5">{{ t("bank.link") }}</Button>
    </form>

    <p v-if="accounts.length === 0" class="text-muted">{{ t("bank.empty") }}</p>
    <table v-else class="w-full border-collapse text-sm">
      <thead>
        <tr class="border-b border-rule text-left font-mono text-xs uppercase tracking-[0.2em] text-muted">
          <th class="py-3 pr-4">{{ t("bank.name") }}</th>
          <th class="py-3 pr-4">{{ t("bank.number") }}</th>
          <th class="hidden py-3 pr-4 md:table-cell">{{ t("bank.added") }}</th>
          <th class="py-3 text-right"><span class="sr-only">Unlink</span></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in accounts" :key="a.bank_account_id" class="border-b border-rule">
          <td class="py-3 pr-4 font-medium text-ink">{{ a.bank_name }}</td>
          <td class="py-3 pr-4 font-mono">{{ a.account_number_masked }}</td>
          <td class="hidden py-3 pr-4 font-mono text-xs text-muted md:table-cell">{{ fmtShortDate(a.created_at ?? null) }}</td>
          <td class="py-3 text-right">
            <button
              type="button"
              class="rounded-full border border-rule px-3 py-1 font-mono text-xs text-muted transition-colors hover:border-down hover:text-down"
              @click="unlink(a)"
            >
              {{ t("bank.unlink") }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
