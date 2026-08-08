<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useI18n } from "../i18n";
import Button from "../components/ui/Button.vue";
import Input from "../components/ui/Input.vue";
import Select from "../components/ui/Select.vue";
import Badge from "../components/ui/Badge.vue";
import { api } from "../lib/api";
import { fmtMoney, fmtPrice, fmtQty, fmtDate, signed, dirClass } from "../lib/format";
import type { Portfolio, Holding, Summary, ActivityEvent, BankAccount } from "../lib/types";

const { t } = useI18n();

const portfolios = ref<Portfolio[]>([]);
const activeId = ref("");
const summary = ref<Summary | null>(null);
const holdings = ref<Holding[]>([]);
const activity = ref<ActivityEvent[]>([]);
const banks = ref<BankAccount[]>([]);
const loading = ref(true);
const error = ref("");

const newName = ref("");
const renameName = ref("");
const amount = ref("");
const bankAccountId = ref("");
const msg = ref("");
const busy = ref(false);

const active = () => portfolios.value.find((p) => p.portfolio_id === activeId.value);

async function loadPortfolios() {
  try {
    portfolios.value = await api<Portfolio[]>("/portfolios");
    if (!activeId.value || !portfolios.value.some((p) => p.portfolio_id === activeId.value)) {
      activeId.value = portfolios.value[0]?.portfolio_id ?? "";
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  } finally {
    loading.value = false;
  }
}

async function loadDetail() {
  if (!activeId.value) return;
  error.value = "";
  try {
    const [s, h, a] = await Promise.all([
      api<Summary>(`/portfolios/${activeId.value}/summary`),
      api<Holding[]>(`/portfolios/${activeId.value}/holdings`),
      api<ActivityEvent[]>(`/portfolios/${activeId.value}/activity`),
    ]);
    summary.value = s;
    holdings.value = h;
    activity.value = a;
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  }
}

async function loadBanks() {
  try {
    banks.value = await api<BankAccount[]>("/bank-accounts");
  } catch {
    /* optional */
  }
}

async function createPortfolio() {
  msg.value = "";
  try {
    await api("/portfolios", { body: { name: newName.value } });
    newName.value = "";
    await loadPortfolios();
  } catch (e) {
    msg.value = e instanceof Error ? e.message : "Error";
  }
}

async function renamePortfolio() {
  msg.value = "";
  try {
    await api(`/portfolios/${activeId.value}`, { method: "PUT", body: { name: renameName.value } });
    await loadPortfolios();
  } catch (e) {
    msg.value = e instanceof Error ? e.message : "Error";
  }
}

async function deletePortfolio() {
  if (!activeId.value) return;
  msg.value = "";
  try {
    await api(`/portfolios/${activeId.value}`, { method: "DELETE" });
    activeId.value = "";
    summary.value = null;
    holdings.value = [];
    activity.value = [];
    await loadPortfolios();
  } catch (e) {
    msg.value = e instanceof Error ? e.message : "Error";
  }
}

async function moveCash(kind: "deposit" | "withdraw") {
  if (!activeId.value) return;
  msg.value = "";
  busy.value = true;
  try {
    const body: Record<string, unknown> = { amount: Number(amount.value) };
    if (bankAccountId.value) body.bank_account_id = bankAccountId.value;
    await api(`/portfolios/${activeId.value}/${kind}`, { body });
    amount.value = "";
    await loadPortfolios();
    await loadDetail();
  } catch (e) {
    msg.value = e instanceof Error ? e.message : "Error";
  } finally {
    busy.value = false;
  }
}

watch(activeId, loadDetail);
onMounted(async () => {
  await Promise.all([loadPortfolios(), loadBanks()]);
  if (activeId.value) loadDetail();
});
</script>

<template>
  <div class="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
    <header class="pb-10">
      <p class="font-mono text-xs uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
      <h1 class="mt-3 font-display text-3xl font-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("nav.portfolio") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("portfolio.subtitle") }}</p>
    </header>

    <p v-if="error" class="mb-4 font-mono text-sm text-down">{{ error }}</p>
    <p v-if="msg" class="mb-4 font-mono text-sm text-down">{{ msg }}</p>
    <p v-if="loading" class="text-muted">{{ t("news.loading") }}</p>

    <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <aside class="flex flex-col gap-6">
        <section class="rounded-2xl border border-rule bg-paper-2 p-6">
          <h2 class="font-display text-xl font-bold tracking-[-0.02em] text-ink">{{ t("portfolio.select") }}</h2>
          <p v-if="portfolios.length === 0" class="mt-4 text-sm text-muted">{{ t("portfolio.empty") }}</p>
          <template v-else>
            <div class="mt-4 flex flex-col gap-2">
              <button
                v-for="p in portfolios"
                :key="p.portfolio_id"
                type="button"
                class="flex items-center justify-between rounded-lg border px-4 py-3 text-left transition-colors duration-150"
                :class="activeId === p.portfolio_id ? 'border-band bg-band text-band-ink' : 'border-rule text-ink hover:bg-paper'"
                @click="activeId = p.portfolio_id"
              >
                <span class="font-medium">{{ p.name }}</span>
                <span class="font-mono text-xs opacity-80">{{ fmtMoney(p.cash_balance) }}</span>
              </button>
            </div>
          </template>

          <form class="mt-5 flex flex-col gap-3 border-t border-rule pt-5" @submit.prevent="createPortfolio">
            <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">{{ t("portfolio.new") }}</span>
            <Input v-model="newName" :placeholder="t('portfolio.namePlaceholder')" required />
            <Button class="w-full">{{ t("portfolio.create") }}</Button>
          </form>
        </section>

        <section v-if="active()" class="rounded-2xl border border-rule bg-paper-2 p-6">
          <h2 class="font-display text-xl font-bold tracking-[-0.02em] text-ink">{{ t("portfolio.manage") }}</h2>
          <div class="mt-4 flex flex-col gap-3">
            <Input v-model="renameName" :placeholder="active()?.name" />
            <div class="flex gap-3">
              <Button variant="outline" class="flex-1" @click="renamePortfolio">{{ t("portfolio.rename") }}</Button>
              <Button variant="ghost" class="flex-1 text-down" @click="deletePortfolio">{{ t("portfolio.delete") }}</Button>
            </div>
          </div>
        </section>
      </aside>

      <div class="flex flex-col gap-6 lg:col-span-2">
        <section v-if="summary" class="rounded-2xl border border-rule bg-paper-2 p-6">
          <div class="flex flex-wrap items-end justify-between gap-3">
            <div>
              <p class="font-mono text-xs uppercase tracking-[0.2em] text-muted">{{ t("portfolio.total") }}</p>
              <p class="mt-1 font-display text-2xl font-bold tracking-[-0.02em] text-ink">{{ fmtMoney(summary.total_value) }}</p>
            </div>
            <Badge>{{ active()?.name }}</Badge>
          </div>
          <div class="mt-5 grid grid-cols-2 gap-4 border-t border-rule pt-5 sm:grid-cols-4">
            <div class="flex flex-col gap-1">
              <span class="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">{{ t("portfolio.cash") }}</span>
              <span class="font-mono text-sm text-ink">{{ fmtMoney(summary.cash_balance) }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">{{ t("portfolio.holdingsValue") }}</span>
              <span class="font-mono text-sm text-ink">{{ fmtMoney(summary.holdings_value) }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">{{ t("portfolio.realized") }}</span>
              <span class="font-mono text-sm" :class="dirClass(summary.realized_pnl)">{{ signed(summary.realized_pnl) }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">{{ t("portfolio.allocation") }}</span>
              <span class="font-mono text-sm text-ink">{{ summary.allocations.length }}</span>
            </div>
          </div>

          <form class="mt-6 grid grid-cols-1 gap-3 border-t border-rule pt-5 sm:grid-cols-2" @submit.prevent>
            <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted sm:col-span-2">{{ t("portfolio.moveCash") }}</span>
            <Input v-model="amount" type="number" min="0" step="0.01" :placeholder="t('portfolio.amount')" required />
            <Select v-model="bankAccountId">
              <option value="">{{ t("portfolio.noAccounts") }}</option>
              <option v-for="b in banks" :key="b.bank_account_id" :value="b.bank_account_id">
                {{ b.bank_name }} · {{ b.account_number_masked }}
              </option>
            </Select>
            <div class="flex gap-3 sm:col-span-2">
              <Button type="button" :disabled="busy" class="flex-1" @click="moveCash('deposit')">{{ t("portfolio.deposit") }}</Button>
              <Button type="button" :disabled="busy" variant="outline" class="flex-1" @click="moveCash('withdraw')">{{ t("portfolio.withdraw") }}</Button>
            </div>
          </form>
        </section>

        <section class="rounded-2xl border border-rule bg-paper-2 p-6">
          <h2 class="font-display text-xl font-bold tracking-[-0.02em] text-ink">{{ t("portfolio.holdings") }}</h2>
          <p v-if="holdings.length === 0" class="mt-4 text-sm text-muted">{{ t("portfolio.noHoldings") }}</p>
          <table v-else class="mt-4 w-full border-collapse text-sm">
            <thead>
              <tr class="border-b border-rule text-left font-mono text-xs uppercase tracking-[0.2em] text-muted">
                <th class="py-2 pr-4">{{ t("market.ticker") }}</th>
                <th class="hidden py-2 pr-4 text-right md:table-cell">{{ t("portfolio.qty") }}</th>
                <th class="hidden py-2 pr-4 text-right sm:table-cell">{{ t("portfolio.avgCost") }}</th>
                <th class="py-2 pr-4 text-right">{{ t("portfolio.current") }}</th>
                <th class="hidden py-2 pr-4 text-right sm:table-cell">{{ t("portfolio.marketValue") }}</th>
                <th class="py-2 text-right">{{ t("portfolio.pnl") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="h in holdings" :key="h.stock_id" class="border-b border-rule">
                <td class="py-2 pr-4">
                  <RouterLink :to="`/stocks/${h.ticker}`" class="font-mono font-semibold text-ink hover:text-band">{{ h.ticker }}</RouterLink>
                  <p class="text-xs text-muted">{{ h.company_name }}</p>
                </td>
                <td class="hidden py-2 pr-4 text-right font-mono md:table-cell">{{ fmtQty(h.quantity) }}</td>
                <td class="hidden py-2 pr-4 text-right font-mono sm:table-cell">{{ fmtPrice(h.avg_cost) }}</td>
                <td class="py-2 pr-4 text-right font-mono">{{ fmtPrice(h.current_price) }}</td>
                <td class="hidden py-2 pr-4 text-right font-mono sm:table-cell">{{ fmtPrice(h.market_value) }}</td>
                <td class="py-2 text-right font-mono" :class="dirClass(h.unrealized_pnl)">{{ signed(h.unrealized_pnl) }}</td>
              </tr>
            </tbody>
          </table>
        </section>

        <section class="rounded-2xl border border-rule bg-paper-2 p-6">
          <h2 class="font-display text-xl font-bold tracking-[-0.02em] text-ink">{{ t("portfolio.activity") }}</h2>
          <p v-if="activity.length === 0" class="mt-4 text-sm text-muted">{{ t("portfolio.noActivity") }}</p>
          <table v-else class="mt-4 w-full border-collapse text-sm">
            <thead>
              <tr class="border-b border-rule text-left font-mono text-xs uppercase tracking-[0.2em] text-muted">
                <th class="py-2 pr-4">{{ t("portfolio.type") }}</th>
                <th class="py-2 pr-4 text-right">{{ t("portfolio.amount") }}</th>
                <th class="hidden py-2 pr-4 sm:table-cell">{{ t("market.ticker") }}</th>
                <th class="py-2 text-right">{{ t("portfolio.date") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(ev, i) in activity" :key="i" class="border-b border-rule">
                <td class="py-2 pr-4">
                  <Badge>{{ ev.type }}</Badge>
                </td>
                <td class="py-2 pr-4 text-right font-mono">{{ fmtPrice(ev.amount) }}</td>
                <td class="hidden py-2 pr-4 font-mono sm:table-cell">{{ ev.ticker ?? "—" }}</td>
                <td class="py-2 text-right font-mono text-xs text-muted">{{ fmtDate(ev.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </section>
      </div>
    </div>
  </div>
</template>
