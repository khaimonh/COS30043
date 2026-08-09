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
  <div class="mx-auto w-100 max-w-6xl px-3 pb-5 pt-5 px-sm-4 pt-sm-5">
    <header class="pb-5">
      <p class="font-mono text-xs text-uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
      <h1 class="mt-3 font-display text-3xl fw-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("nav.portfolio") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("portfolio.subtitle") }}</p>
    </header>

    <p v-if="error" class="mb-3 font-mono text-sm text-down">{{ error }}</p>
    <p v-if="msg" class="mb-3 font-mono text-sm text-down">{{ msg }}</p>
    <p v-if="loading" class="text-muted">{{ t("news.loading") }}</p>

    <div v-else class="row g-4">
      <aside class="d-flex flex-column gap-4 col-lg-4">
        <section class="rounded-4 border border-rule bg-paper-2 p-4">
          <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("portfolio.select") }}</h2>
          <p v-if="portfolios.length === 0" class="mt-3 text-sm text-muted">{{ t("portfolio.empty") }}</p>
          <template v-else>
            <div class="mt-3 d-flex flex-column gap-2">
              <button
                v-for="p in portfolios"
                :key="p.portfolio_id"
                type="button"
                class="d-flex align-items-center justify-content-between rounded-3 border px-3 py-3 text-start transition-colors duration-150"
                :class="activeId === p.portfolio_id ? 'border-band bg-band text-band-ink' : 'border-rule text-ink hover:bg-paper'"
                @click="activeId = p.portfolio_id"
              >
                <span class="fw-medium">{{ p.name }}</span>
                <span class="font-mono text-xs opacity-80">{{ fmtMoney(p.cash_balance) }}</span>
              </button>
            </div>
          </template>

          <form class="mt-3 d-flex flex-column gap-3 border-top border-rule pt-3" @submit.prevent="createPortfolio">
            <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("portfolio.new") }}</span>
            <Input v-model="newName" :placeholder="t('portfolio.namePlaceholder')" required />
            <Button class="w-100">{{ t("portfolio.create") }}</Button>
          </form>
        </section>

        <section v-if="active()" class="rounded-4 border border-rule bg-paper-2 p-4">
          <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("portfolio.manage") }}</h2>
          <div class="mt-3 d-flex flex-column gap-3">
            <Input v-model="renameName" :placeholder="active()?.name" />
            <div class="d-flex gap-3">
              <Button variant="outline" class="flex-grow-1" @click="renamePortfolio">{{ t("portfolio.rename") }}</Button>
              <Button variant="ghost" class="flex-grow-1 text-down" @click="deletePortfolio">{{ t("portfolio.delete") }}</Button>
            </div>
          </div>
        </section>
      </aside>

      <div class="d-flex flex-column gap-4 col-lg-8">
        <section v-if="summary" class="rounded-4 border border-rule bg-paper-2 p-4">
          <div class="d-flex flex-wrap align-items-end justify-content-between gap-3">
            <div>
              <p class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("portfolio.total") }}</p>
              <p class="mt-1 font-display text-2xl fw-bold tracking-[-0.02em] text-ink">{{ fmtMoney(summary.total_value) }}</p>
            </div>
            <Badge>{{ active()?.name }}</Badge>
          </div>
          <div class="mt-3 row row-cols-2 row-cols-sm-4 g-4 border-top border-rule pt-3">
            <div class="d-flex flex-column gap-1">
              <span class="font-mono text-[11px] text-uppercase tracking-[0.2em] text-muted">{{ t("portfolio.cash") }}</span>
              <span class="font-mono text-sm text-ink">{{ fmtMoney(summary.cash_balance) }}</span>
            </div>
            <div class="d-flex flex-column gap-1">
              <span class="font-mono text-[11px] text-uppercase tracking-[0.2em] text-muted">{{ t("portfolio.holdingsValue") }}</span>
              <span class="font-mono text-sm text-ink">{{ fmtMoney(summary.holdings_value) }}</span>
            </div>
            <div class="d-flex flex-column gap-1">
              <span class="font-mono text-[11px] text-uppercase tracking-[0.2em] text-muted">{{ t("portfolio.realized") }}</span>
              <span class="font-mono text-sm" :class="dirClass(summary.realized_pnl)">{{ signed(summary.realized_pnl) }}</span>
            </div>
            <div class="d-flex flex-column gap-1">
              <span class="font-mono text-[11px] text-uppercase tracking-[0.2em] text-muted">{{ t("portfolio.allocation") }}</span>
              <span class="font-mono text-sm text-ink">{{ summary.allocations.length }}</span>
            </div>
          </div>

          <form class="mt-4 row row-cols-1 row-cols-sm-2 g-3 border-top border-rule pt-3" @submit.prevent>
            <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted col-sm-12">{{ t("portfolio.moveCash") }}</span>
            <Input v-model="amount" type="number" min="0" step="0.01" :placeholder="t('portfolio.amount')" required />
            <Select v-model="bankAccountId">
              <option value="">{{ t("portfolio.noAccounts") }}</option>
              <option v-for="b in banks" :key="b.bank_account_id" :value="b.bank_account_id">
                {{ b.bank_name }} · {{ b.account_number_masked }}
              </option>
            </Select>
            <div class="d-flex gap-3 col-sm-12">
              <Button type="button" :disabled="busy" class="flex-grow-1" @click="moveCash('deposit')">{{ t("portfolio.deposit") }}</Button>
              <Button type="button" :disabled="busy" variant="outline" class="flex-grow-1" @click="moveCash('withdraw')">{{ t("portfolio.withdraw") }}</Button>
            </div>
          </form>
        </section>

        <section class="rounded-4 border border-rule bg-paper-2 p-4">
          <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("portfolio.holdings") }}</h2>
          <p v-if="holdings.length === 0" class="mt-3 text-sm text-muted">{{ t("portfolio.noHoldings") }}</p>
          <table v-else class="mt-3 w-100 border-collapse text-sm">
            <thead>
              <tr class="border-bottom border-rule text-start font-mono text-xs text-uppercase tracking-[0.2em] text-muted">
                <th class="py-2 pe-3">{{ t("market.ticker") }}</th>
                <th class="d-none py-2 pe-3 text-end d-md-table-cell">{{ t("portfolio.qty") }}</th>
                <th class="d-none py-2 pe-3 text-end d-sm-table-cell">{{ t("portfolio.avgCost") }}</th>
                <th class="py-2 pe-3 text-end">{{ t("portfolio.current") }}</th>
                <th class="d-none py-2 pe-3 text-end d-sm-table-cell">{{ t("portfolio.marketValue") }}</th>
                <th class="py-2 text-end">{{ t("portfolio.pnl") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="h in holdings" :key="h.stock_id" class="border-bottom border-rule">
                <td class="py-2 pe-3">
                  <RouterLink :to="`/stocks/${h.ticker}`" class="font-mono fw-semibold text-ink hover:text-band">{{ h.ticker }}</RouterLink>
                  <p class="text-xs text-muted">{{ h.company_name }}</p>
                </td>
                <td class="d-none py-2 pe-3 text-end font-mono d-md-table-cell">{{ fmtQty(h.quantity) }}</td>
                <td class="d-none py-2 pe-3 text-end font-mono d-sm-table-cell">{{ fmtPrice(h.avg_cost) }}</td>
                <td class="py-2 pe-3 text-end font-mono">{{ fmtPrice(h.current_price) }}</td>
                <td class="d-none py-2 pe-3 text-end font-mono d-sm-table-cell">{{ fmtMoney(h.market_value) }}</td>
                <td class="py-2 text-end font-mono" :class="dirClass(h.unrealized_pnl)">{{ signed(h.unrealized_pnl) }}</td>
              </tr>
            </tbody>
          </table>
        </section>

        <section class="rounded-4 border border-rule bg-paper-2 p-4">
          <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("portfolio.activity") }}</h2>
          <p v-if="activity.length === 0" class="mt-3 text-sm text-muted">{{ t("portfolio.noActivity") }}</p>
          <table v-else class="mt-3 w-100 border-collapse text-sm">
            <thead>
              <tr class="border-bottom border-rule text-start font-mono text-xs text-uppercase tracking-[0.2em] text-muted">
                <th class="py-2 pe-3">{{ t("portfolio.type") }}</th>
                <th class="py-2 pe-3 text-end">{{ t("portfolio.amount") }}</th>
                <th class="d-none py-2 pe-3 d-sm-table-cell">{{ t("market.ticker") }}</th>
                <th class="py-2 text-end">{{ t("portfolio.date") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(ev, i) in activity" :key="i" class="border-bottom border-rule">
                <td class="py-2 pe-3">
                  <Badge>{{ ev.type }}</Badge>
                </td>
                <td class="py-2 pe-3 text-end font-mono">{{ fmtMoney(ev.amount) }}</td>
                <td class="d-none py-2 pe-3 font-mono d-sm-table-cell">{{ ev.ticker ?? "—" }}</td>
                <td class="py-2 text-end font-mono text-xs text-muted">{{ fmtDate(ev.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </section>
      </div>
    </div>
  </div>
</template>
