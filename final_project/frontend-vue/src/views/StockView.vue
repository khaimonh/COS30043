<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useI18n } from "../i18n";
import Button from "../components/ui/Button.vue";
import Input from "../components/ui/Input.vue";
import Select from "../components/ui/Select.vue";
import CandleChart from "../components/ui/CandleChart.vue";
import { api } from "../lib/api";
import { token } from "../lib/session";
import { fmtPrice, fmtQty, fmtShortDate, signed, dirClass, num } from "../lib/format";
import type { Stock, Quote, HistoryPoint, Portfolio, WatchlistEntry } from "../lib/types";

const { t, tf } = useI18n();
const route = useRoute();

const ticker = computed(() => String(route.params.ticker));
const stock = ref<Stock | null>(null);
const quote = ref<Quote | null>(null);
const history = ref<HistoryPoint[]>([]);
const portfolios = ref<Portfolio[]>([]);
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

async function loadAll() {
  loading.value = true;
  error.value = "";
  try {
    const [s, q, h] = await Promise.all([
      api<Stock>(`/stocks/${ticker.value}`),
      api<Quote>(`/stocks/${ticker.value}/quote`).catch(() => null),
      api<{ points: HistoryPoint[] }>(`/stocks/${ticker.value}/history?limit=60`),
    ]);
    stock.value = s;
    quote.value = q;
    history.value = h.points;
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  } finally {
    loading.value = false;
  }
  if (token.value) {
    loadWatchStatus();
    loadPortfolios();
  }
}

async function loadWatchStatus() {
  try {
    const list = await api<WatchlistEntry[]>("/watchlist");
    watchEntry.value = list.find((w) => w.ticker === ticker.value) ?? null;
    if (watchEntry.value) targetPrice.value = watchEntry.value.target_price ? String((num(watchEntry.value.target_price) ?? 0) / 1000) : "";
  } catch {
    /* ignore */
  }
}

async function loadPortfolios() {
  try {
    portfolios.value = await api<Portfolio[]>("/portfolios");
    if (portfolios.value.length && !portfolios.value.some((p) => p.portfolio_id === portfolioId.value)) {
      portfolioId.value = portfolios.value[0].portfolio_id;
    }
  } catch {
    /* ignore */
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

onMounted(() => {
  loadAll();
});
watch(ticker, () => {
  loadAll();
});
</script>

<template>
  <div class="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
    <p v-if="error" class="mb-4 font-mono text-sm text-down">{{ error }}</p>
    <p v-if="loading" class="text-muted">{{ t("news.loading") }}</p>

    <template v-if="stock">
      <header class="pb-8">
        <p class="font-mono text-xs uppercase tracking-[0.25em] text-muted">{{ t("nav.market") }}</p>
        <div class="mt-3 flex flex-wrap items-end gap-x-6 gap-y-2">
          <h1 class="font-display text-3xl font-bold tracking-[-0.02em] text-ink sm:text-5xl">{{ stock.ticker }}</h1>
          <div class="pb-1 text-left">
            <p class="text-sm text-muted">{{ stock.company_name }}</p>
            <p class="font-mono text-xs text-muted">{{ stock.exchange }} · {{ stock.sector }}</p>
          </div>
        </div>

        <div class="mt-5 flex flex-wrap items-baseline gap-x-4 gap-y-2">
          <span class="font-mono text-3xl font-semibold tracking-tight text-ink tabular-nums">{{ fmtPrice(quote?.close_price) }}</span>
          <span class="font-mono text-sm" :class="dirClass(change)">{{ signed(change) }}</span>
          <span class="font-mono text-xs text-muted">{{ stock.exchange }} · {{ stock.sector }}</span>
        </div>
      </header>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-5">
        <section class="rounded-2xl border border-rule bg-paper-2 p-6 lg:col-span-3">
          <div class="flex items-baseline justify-between gap-3">
            <h2 class="font-display text-xl font-bold tracking-[-0.02em] text-ink">{{ t("stock.history") }}</h2>
            <p class="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">{{ t("market.liveNote") }}</p>
          </div>

          <div v-if="history.length > 0" class="mt-5">
            <CandleChart :points="history" />
          </div>
          <div v-else class="mt-6 text-sm text-muted">{{ t("market.empty") }}</div>

          <dl class="mt-5 grid grid-cols-2 gap-4 border-y border-rule py-4 sm:grid-cols-4">
            <div v-for="stat in [
              { label: t('stock.open'), value: fmtPrice(quote?.open_price) },
              { label: t('stock.high'), value: fmtPrice(quote?.high_price) },
              { label: t('stock.low'), value: fmtPrice(quote?.low_price) },
              { label: t('stock.volume'), value: fmtQty(quote?.volume_accumulated) },
            ]" :key="stat.label" class="flex flex-col gap-1">
              <dt class="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">{{ stat.label }}</dt>
              <dd class="font-mono text-sm text-ink tabular-nums">{{ stat.value }}</dd>
            </div>
          </dl>

          <table v-if="history.length > 0" class="mt-2 w-full border-collapse text-sm">
            <thead>
              <tr class="border-b border-rule text-left font-mono text-xs uppercase tracking-[0.2em] text-muted">
                <th class="py-2 pr-4">{{ t("stock.date") }}</th>
                <th class="hidden py-2 pr-4 text-right sm:table-cell">{{ t("stock.open") }}</th>
                <th class="hidden py-2 pr-4 text-right sm:table-cell">{{ t("stock.high") }}</th>
                <th class="hidden py-2 pr-4 text-right sm:table-cell">{{ t("stock.low") }}</th>
                <th class="py-2 pr-4 text-right">{{ t("stock.close") }}</th>
                <th class="py-2 text-right">{{ t("stock.volume") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, i) in history" :key="p.time ?? i" class="border-b border-rule">
                <td class="py-2 pr-4 font-mono text-xs text-muted">{{ fmtShortDate(p.time) }}</td>
                <td class="hidden py-2 pr-4 text-right font-mono tabular-nums sm:table-cell">{{ fmtPrice(p.open) }}</td>
                <td class="hidden py-2 pr-4 text-right font-mono tabular-nums sm:table-cell">{{ fmtPrice(p.high) }}</td>
                <td class="hidden py-2 pr-4 text-right font-mono tabular-nums sm:table-cell">{{ fmtPrice(p.low) }}</td>
                <td class="py-2 pr-4 text-right font-mono font-semibold tabular-nums text-ink">{{ fmtPrice(p.close) }}</td>
                <td class="py-2 text-right font-mono text-xs tabular-nums text-muted">{{ fmtQty(p.volume) }}</td>
              </tr>
            </tbody>
          </table>
        </section>

        <aside class="flex flex-col gap-6 lg:col-span-2">
          <section class="rounded-2xl border border-rule bg-paper-2 p-6">
            <h2 class="font-display text-xl font-bold tracking-[-0.02em] text-ink">{{ t("stock.orderTitle") }}</h2>

            <p v-if="!token" class="mt-4 text-sm text-muted">{{ t("stock.noAuth") }}</p>
            <div v-else-if="portfolios.length === 0" class="mt-4 text-sm text-muted">
              {{ t("stock.noPortfolio") }}
              <RouterLink to="/portfolio" class="font-mono text-band underline underline-offset-4">{{ t("nav.portfolio") }}</RouterLink>
            </div>
            <form v-else class="mt-4 flex flex-col gap-4" @submit.prevent="placeOrder">
              <div class="grid grid-cols-2 gap-3">
                <button
                  v-for="ty in ['Buy', 'Sell']"
                  :key="ty"
                  type="button"
                  class="rounded-full border px-4 py-2 font-mono text-sm transition-colors duration-150"
                  :class="orderType === ty ? 'border-band bg-band text-band-ink' : 'border-rule text-muted hover:text-ink'"
                  @click="orderType = ty"
                >
                  {{ t(ty === 'Buy' ? 'stock.buy' : 'stock.sell') }}
                </button>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <button
                  v-for="st in ['Market', 'Limit']"
                  :key="st"
                  type="button"
                  class="rounded-full border px-4 py-2 font-mono text-sm transition-colors duration-150"
                  :class="orderStyle === st ? 'border-band bg-band text-band-ink' : 'border-rule text-muted hover:text-ink'"
                  @click="orderStyle = st"
                >
                  {{ t(st === 'Market' ? 'stock.market' : 'stock.limit') }}
                </button>
              </div>
              <label class="flex flex-col gap-1.5">
                <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">{{ t("nav.portfolio") }}</span>
                <Select v-model="portfolioId" required>
                  <option v-for="p in portfolios" :key="p.portfolio_id" :value="p.portfolio_id">{{ p.name }}</option>
                </Select>
              </label>
              <label class="flex flex-col gap-1.5">
                <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">{{ t("stock.quantity") }}</span>
                <Input v-model.number="quantity" type="number" min="1" step="1" required />
              </label>
              <label v-if="orderStyle === 'Limit'" class="flex flex-col gap-1.5">
                <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">{{ t("stock.limitPrice") }}</span>
                <Input v-model="limitPrice" type="number" min="0" step="0.01" required />
              </label>
              <p v-if="orderMsg" class="font-mono text-sm" :class="orderOk ? 'text-up' : 'text-down'">{{ orderMsg }}</p>
              <Button :disabled="placing" class="w-full">{{ t("stock.placeOrder") }}</Button>
            </form>
          </section>

          <section class="rounded-2xl border border-rule bg-paper-2 p-6">
            <h2 class="font-display text-xl font-bold tracking-[-0.02em] text-ink">{{ t("stock.watchTitle") }}</h2>
            <p v-if="!token" class="mt-4 text-sm text-muted">{{ t("stock.noAuth") }}</p>
            <div v-else class="mt-4 flex flex-col gap-3">
              <label class="flex flex-col gap-1.5">
                <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">{{ t("stock.target") }}</span>
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
