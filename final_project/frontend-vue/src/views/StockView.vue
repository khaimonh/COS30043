<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useI18n } from "../i18n";
import Button from "../components/ui/Button.vue";
import Input from "../components/ui/Input.vue";
import Select from "../components/ui/Select.vue";
import CandleChart from "../components/ui/CandleChart.vue";
import { api } from "../lib/api";
import { token, ensureUser } from "../lib/session";
import { fmtPrice, fmtQty, fmtShortDate, signed, dirClass, num } from "../lib/format";
import { quoteFor, subscribeTickers, unsubscribeTickers, connected as wsConnected } from "../lib/quotes";
import type { Stock, Quote, HistoryPoint, Portfolio, WatchlistEntry } from "../lib/types";

const { t, tf } = useI18n();
const route = useRoute();

const ticker = computed(() => String(route.params.ticker));
const stock = ref<Stock | null>(null);
const httpQuote = ref<Quote | null>(null);
const quote = computed<Quote | null>(() => quoteFor(ticker.value) ?? httpQuote.value);
const history = ref<HistoryPoint[]>([]);
const portfolios = ref<Portfolio[]>([]);
const historyLoading = ref(true);
const portfolioLoading = ref(true);
const watchEntry = ref<WatchlistEntry | null>(null);
const loading = ref(true);
const error = ref("");
const orderMsg = ref("");
const orderOk = ref(false);
const watchMsg = ref("");

const orderType = ref("Buy");
const orderStyle = ref("Market");
const quantity = ref<number>(100);
const limitPrice = ref<string>("");
const portfolioId = ref("");
const targetPrice = ref<string>("");
const placing = ref(false);

async function loadQuote() {
  httpQuote.value = await api<Quote>(`/stocks/${ticker.value}/quote`).catch(() => null);
}

async function loadAll() {
  loading.value = true;
  error.value = "";

  try {
    const [s, h] = await Promise.all([
      api<Stock>(`/stocks/${ticker.value}`),
      api<{ points: HistoryPoint[] }>(
        `/stocks/${ticker.value}/history?limit=60`
      ),
    ]);

    stock.value = s;
    history.value = h.points;

    await loadQuote();

    if (token.value) {
      await ensureUser();

      await Promise.all([
        loadWatchStatus(),
        loadPortfolios(),
      ]);
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  } finally {
    loading.value = false;
    historyLoading.value = false;
  }
}

async function loadWatchStatus() {
  try {
    const list = await api<WatchlistEntry[]>("/watchlist");
    watchEntry.value = list.find((w) => w.ticker === ticker.value) ?? null;
    if (watchEntry.value) targetPrice.value = watchEntry.value.target_price ? String((num(watchEntry.value.target_price) ?? 0) / 1000) : "";
  } catch {
  }
}

async function loadPortfolios() {
  try {
    portfolios.value = await api<Portfolio[]>("/portfolios/");
    if (portfolios.value.length && !portfolios.value.some((p) => p.portfolio_id === portfolioId.value)) {
      portfolioId.value = portfolios.value[0].portfolio_id;
    }
  } catch (e) {
    console.error("Failed to load portfolios:", e);
  } finally {
    portfolioLoading.value = false;
  }
}

async function placeOrder() {
  orderMsg.value = "";
  orderOk.value = false;
  placing.value = true;
  try {
    const body: Record<string, unknown> = {
      portfolio_id: portfolioId.value,
      stock_ticker: ticker.value,
      order_type: orderType.value,
      order_style: orderStyle.value,
      quantity: Number(quantity.value),
    };
    if (orderStyle.value === "Limit") body.limit_price = Number(limitPrice.value) * 1000;
    const res = await api<{ order_id: string }>("/orders", { body });
    orderMsg.value = tf("stock.orderSent", { id: res.order_id.slice(0, 8) });
    orderOk.value = true;
  } catch (e) {
    orderMsg.value = e instanceof Error ? e.message : "Error";
  } finally {
    placing.value = false;
  }
}

async function toggleWatch() {
  watchMsg.value = "";
  try {
    if (watchEntry.value) {
      await api(`/watchlist/${watchEntry.value.watchlist_id}`, { method: "DELETE" });
      watchEntry.value = null;
      targetPrice.value = "";
    } else {
      const body: Record<string, unknown> = { ticker: ticker.value };
      if (targetPrice.value) body.target_price = Number(targetPrice.value) * 1000;
      watchEntry.value = await api<WatchlistEntry>("/watchlist", { body });
    }
  } catch (e) {
    watchMsg.value = e instanceof Error ? e.message : "Error";
  }
}

const change = computed(() => quote.value?.change ?? quote.value?.change_price ?? quote.value?.pct_change ?? null);

const historyDesc = computed(() =>
  [...history.value].sort((a, b) => (Date.parse(String(b.time)) || 0) - (Date.parse(String(a.time)) || 0))
);

const POLL_MS = 15000;
let pollTimer: number | undefined;

onMounted(() => {
  subscribeTickers([ticker.value]);
  pollTimer = window.setInterval(() => {
    if (!wsConnected.value) loadQuote();
  }, POLL_MS);
  loadAll();
});
watch(ticker, (next, prev) => {
  if (prev) unsubscribeTickers([prev]);
  subscribeTickers([next]);
  loadAll();
});
onBeforeUnmount(() => {
  unsubscribeTickers([ticker.value]);
  window.clearInterval(pollTimer);
});
</script>

<template>
  <div class="mx-auto w-100 max-w-6xl px-3 pb-5 pt-5 px-sm-4 pt-sm-5">
    <p v-if="error" class="mb-3 font-mono text-sm text-down">{{ error }}</p>
    <p v-if="loading" class="text-muted">{{ t("news.loading") }}</p>

    <template v-if="stock">
      <header class="pb-5">
        <p class="font-mono text-xs text-uppercase tracking-[0.25em] text-muted">{{ t("nav.market") }}</p>
        <div class="mt-3 d-flex flex-wrap align-items-end gap-x-6 gap-y-2">
          <h1 class="font-display text-3xl fw-bold tracking-[-0.02em] text-ink sm:text-5xl">{{ stock.ticker }}</h1>
          <div class="pb-1 text-start">
            <p class="text-sm text-muted">{{ stock.company_name }}</p>
            <p class="font-mono text-xs text-muted">{{ stock.exchange }} · {{ stock.sector }}</p>
          </div>
        </div>

        <div class="mt-3 d-flex flex-wrap align-items-baseline gap-x-4 gap-y-2">
          <span class="font-mono text-3xl fw-semibold tracking-tight text-ink tabular-nums">{{ fmtPrice(quote?.close_price) }}</span>
          <span class="font-mono text-sm" :class="dirClass(change)">{{ signed(change) }}</span>
          <span class="font-mono text-xs text-muted">{{ stock.exchange }} · {{ stock.sector }}</span>
        </div>
      </header>

      <div class="row g-4">
        <section class="rounded-4 border border-rule bg-paper-2 p-4 col-lg-5">
          <div class="d-flex align-items-baseline justify-content-between gap-3">
            <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("stock.history") }}</h2>
            <p class="font-mono text-[11px] text-uppercase tracking-[0.2em] text-muted">{{ t("market.liveNote") }}</p>
          </div>

          <div v-if="historyLoading" class="mt-4 text-sm text-muted">{{ t("news.loading") }}</div>
          <div v-else-if="history.length > 0" class="mt-3">
            <CandleChart :points="history" />
          </div>
          <div v-else class="mt-4 text-sm text-muted">{{ t("market.empty") }}</div>

          <dl class="mt-3 row row-cols-2 row-cols-sm-4 g-4 border-top border-bottom border-rule py-3">
            <div v-for="stat in [
              { label: t('stock.open'), value: fmtPrice(quote?.open_price) },
              { label: t('stock.high'), value: fmtPrice(quote?.high_price) },
              { label: t('stock.low'), value: fmtPrice(quote?.low_price) },
              { label: t('stock.volume'), value: fmtQty(quote?.volume_accumulated) },
            ]" :key="stat.label" class="d-flex flex-column gap-1">
              <dt class="font-mono text-[11px] text-uppercase tracking-[0.2em] text-muted">{{ stat.label }}</dt>
              <dd class="font-mono text-sm text-ink tabular-nums">{{ stat.value }}</dd>
            </div>
          </dl>

          <table v-if="history.length > 0" class="mt-2 w-100 border-collapse text-sm">
            <thead>
              <tr class="border-bottom border-rule text-start font-mono text-xs text-uppercase tracking-[0.2em] text-muted">
                <th class="py-2 pe-3">{{ t("stock.date") }}</th>
                <th class="d-none py-2 pe-3 text-end d-sm-table-cell">{{ t("stock.open") }}</th>
                <th class="d-none py-2 pe-3 text-end d-sm-table-cell">{{ t("stock.high") }}</th>
                <th class="d-none py-2 pe-3 text-end d-sm-table-cell">{{ t("stock.low") }}</th>
                <th class="py-2 pe-3 text-end">{{ t("stock.close") }}</th>
                <th class="py-2 text-end">{{ t("stock.volume") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, i) in historyDesc" :key="p.time ?? i" class="border-bottom border-rule">
                <td class="py-2 pe-3 font-mono text-xs text-muted">{{ fmtShortDate(p.time) }}</td>
                <td class="d-none py-2 pe-3 text-end font-mono tabular-nums d-sm-table-cell">{{ fmtPrice(p.open) }}</td>
                <td class="d-none py-2 pe-3 text-end font-mono tabular-nums d-sm-table-cell">{{ fmtPrice(p.high) }}</td>
                <td class="d-none py-2 pe-3 text-end font-mono tabular-nums d-sm-table-cell">{{ fmtPrice(p.low) }}</td>
                <td class="py-2 pe-3 text-end font-mono fw-semibold tabular-nums text-ink">{{ fmtPrice(p.close) }}</td>
                <td class="py-2 text-end font-mono text-xs tabular-nums text-muted">{{ fmtQty(p.volume) }}</td>
              </tr>
            </tbody>
          </table>
        </section>

        <aside class="d-flex flex-column gap-4 col-lg-2">
          <section class="rounded-4 border border-rule bg-paper-2 p-4">
            <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("stock.orderTitle") }}</h2>

            <p v-if="!token" class="mt-3 text-sm text-muted">
              {{ t("stock.noAuth") }}
              <RouterLink to="/login" class="font-mono text-band underline underline-offset-4">{{ t("nav.login") }}</RouterLink>
            </p>
            <div v-else-if="portfolioLoading" class="mt-3 text-sm text-muted">
              {{ t("news.loading") }}
            </div>
            <div v-else-if="portfolios.length === 0" class="mt-3 text-sm text-muted">
              {{ t("stock.noPortfolio") }}
              <RouterLink to="/portfolio" class="font-mono text-band underline underline-offset-4">{{ t("nav.portfolio") }}</RouterLink>
            </div>
            <form v-else class="mt-3 d-flex flex-column gap-4" @submit.prevent="placeOrder">
              <div class="row row-cols-2 g-3">
                <button
                  v-for="ty in ['Buy', 'Sell']"
                  :key="ty"
                  type="button"
                  class="rounded-pill border px-3 py-2 font-mono text-sm transition-colors duration-150"
                  :class="orderType === ty ? 'border-band bg-band text-band-ink' : 'border-rule text-muted hover:text-ink'"
                  @click="orderType = ty"
                >
                  {{ t(ty === 'Buy' ? 'stock.buy' : 'stock.sell') }}
                </button>
              </div>
              <div class="row row-cols-2 g-3">
                <button
                  v-for="st in ['Market', 'Limit']"
                  :key="st"
                  type="button"
                  class="rounded-pill border px-3 py-2 font-mono text-sm transition-colors duration-150"
                  :class="orderStyle === st ? 'border-band bg-band text-band-ink' : 'border-rule text-muted hover:text-ink'"
                  @click="orderStyle = st"
                >
                  {{ t(st === 'Market' ? 'stock.market' : 'stock.limit') }}
                </button>
              </div>
              <label class="d-flex flex-column gap-1.5">
                <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("nav.portfolio") }}</span>
                <Select v-model="portfolioId" required>
                  <option v-for="p in portfolios" :key="p.portfolio_id" :value="p.portfolio_id">{{ p.name }}</option>
                </Select>
              </label>
              <label class="d-flex flex-column gap-1.5">
                <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("stock.quantity") }}</span>
                <Input v-model.number="quantity" type="number" min="1" step="1" required />
              </label>
              <label v-if="orderStyle === 'Limit'" class="d-flex flex-column gap-1.5">
                <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("stock.limitPrice") }}</span>
                <Input v-model="limitPrice" type="number" min="0" step="0.01" required />
              </label>
              <p v-if="orderMsg" class="font-mono text-sm" :class="orderOk ? 'text-up' : 'text-down'">{{ orderMsg }}</p>
              <Button :disabled="placing" class="w-100">{{ t("stock.placeOrder") }}</Button>
            </form>
          </section>

          <section class="rounded-4 border border-rule bg-paper-2 p-4">
            <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("stock.watchTitle") }}</h2>
            <p v-if="!token" class="mt-3 text-sm text-muted">{{ t("stock.noAuth") }}</p>
            <div v-else class="mt-3 d-flex flex-column gap-3">
              <label class="d-flex flex-column gap-1.5">
                <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("stock.target") }}</span>
                <Input v-model="targetPrice" type="number" min="0" step="0.01" :placeholder="fmtPrice(quote?.close_price)" />
              </label>
              <p v-if="watchMsg" class="font-mono text-sm text-down">{{ watchMsg }}</p>
              <Button :variant="watchEntry ? 'outline' : 'primary'" @click="toggleWatch">
                {{ watchEntry ? t("stock.removeWatch") : t("stock.addWatch") }}
              </Button>
            </div>
          </section>
        </aside>
      </div>
    </template>
  </div>
</template>
