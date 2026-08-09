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
  <div class="mx-auto w-100 max-w-6xl px-3 pb-5 pt-5 px-sm-4 pt-sm-5">
    <header class="pb-5">
      <p class="font-mono text-xs text-uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
      <h1 class="mt-3 font-display text-3xl fw-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("nav.bank") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("bank.subtitle") }}</p>
    </header>

    <p v-if="error" class="mb-3 font-mono text-sm text-down">{{ error }}</p>

    <form class="mb-5 d-flex flex-column gap-3 rounded-4 border border-rule bg-paper-2 p-4 flex-sm-row align-items-sm-end" @submit.prevent="link">
      <label class="d-flex flex-column gap-1.5 sm:max-w-[14rem]">
        <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("bank.name") }}</span>
        <Input v-model="bankName" required />
      </label>
      <label class="d-flex flex-column gap-1.5">
        <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("bank.number") }}</span>
        <Input v-model="accountNumber" inputmode="numeric" required />
      </label>
      <Button :disabled="busy" class="sm:mb-0.5">{{ t("bank.link") }}</Button>
    </form>

    <p v-if="accounts.length === 0" class="text-muted">{{ t("bank.empty") }}</p>
    <table v-else class="w-100 border-collapse text-sm">
      <thead>
        <tr class="border-bottom border-rule text-start font-mono text-xs text-uppercase tracking-[0.2em] text-muted">
          <th class="py-3 pe-3">{{ t("bank.name") }}</th>
          <th class="py-3 pe-3">{{ t("bank.number") }}</th>
          <th class="d-none py-3 pe-3 d-md-table-cell">{{ t("bank.added") }}</th>
          <th class="py-3 text-end"><span class="sr-only">Unlink</span></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in accounts" :key="a.bank_account_id" class="border-bottom border-rule">
          <td class="py-3 pe-3 fw-medium text-ink">{{ a.bank_name }}</td>
          <td class="py-3 pe-3 font-mono">{{ a.account_number_masked }}</td>
          <td class="d-none py-3 pe-3 font-mono text-xs text-muted d-md-table-cell">{{ fmtShortDate(a.created_at ?? null) }}</td>
          <td class="py-3 text-end">
            <button
              type="button"
              class="rounded-pill border border-rule px-3 py-1 font-mono text-xs text-muted transition-colors hover:border-down hover:text-down"
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
