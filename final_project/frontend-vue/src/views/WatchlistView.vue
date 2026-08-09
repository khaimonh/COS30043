<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { useI18n } from "../i18n";
import Button from "../components/ui/Button.vue";
import Input from "../components/ui/Input.vue";
import { api } from "../lib/api";
import { fmtPrice, fmtShortDate, signed, dirClass, num } from "../lib/format";
import { quoteFor, subscribeTickers, unsubscribeTickers, connected as wsConnected } from "../lib/quotes";
import type { WatchlistEntry, Stock } from "../lib/types";

const { t } = useI18n();

const entries = ref<WatchlistEntry[]>([]);
const stocks = ref<Stock[]>([]);
const addTicker = ref("");
const addTarget = ref("");
const msg = ref("");
const busy = ref(false);

async function load() {
  try {
    entries.value = await api<WatchlistEntry[]>("/watchlist");
    subscribeTickers(entries.value.map((e) => e.ticker));
  } catch (e) {
    msg.value = e instanceof Error ? e.message : "Error";
  }
}

async function loadStocks() {
  try {
    stocks.value = await api<Stock[]>("/stocks");
  } catch {
  }
}

async function addEntry() {
  msg.value = "";
  busy.value = true;
  try {
    const body: Record<string, unknown> = { ticker: addTicker.value.trim().toUpperCase() };
    if (addTarget.value) body.target_price = Number(addTarget.value) * 1000;
    await api("/watchlist", { body });
    addTicker.value = "";
    addTarget.value = "";
    await load();
  } catch (e) {
    msg.value = e instanceof Error ? e.message : "Error";
  } finally {
    busy.value = false;
  }
}

async function setTarget(entry: WatchlistEntry, ev: Event) {
  msg.value = "";
  const raw = Number((ev.target as HTMLInputElement).value);
  entry.target_price = Number.isFinite(raw) && raw > 0 ? String(raw * 1000) : "";
  try {
    const body: Record<string, unknown> = {};
    if (entry.target_price) body.target_price = Number(entry.target_price);
    await api(`/watchlist/${entry.watchlist_id}`, { method: "PATCH", body });
    await load();
  } catch (e) {
    msg.value = e instanceof Error ? e.message : "Error";
  }
}

async function remove(entry: WatchlistEntry) {
  msg.value = "";
  try {
    await api(`/watchlist/${entry.watchlist_id}`, { method: "DELETE" });
    await load();
  } catch (e) {
    msg.value = e instanceof Error ? e.message : "Error";
  }
}

function fmtTarget(entry: WatchlistEntry): string {
  const n = num(entry.target_price);
  return n === null ? "" : String(n / 1000);
}

function currentOf(entry: WatchlistEntry): number | null {
  const q = quoteFor(entry.ticker);
  return num(q?.close_price ?? entry.current_price);
}

function distance(entry: WatchlistEntry): number | null {
  const cur = currentOf(entry);
  const target = num(entry.target_price);
  if (cur === null || target === null) return null;
  return cur - target;
}

const POLL_MS = 15000;
let pollTimer: number | undefined;

onMounted(async () => {
  await loadStocks();
  await load();
  pollTimer = window.setInterval(() => {
    if (!wsConnected.value) load();
  }, POLL_MS);
});

onBeforeUnmount(() => {
  unsubscribeTickers(entries.value.map((e) => e.ticker));
  window.clearInterval(pollTimer);
});
</script>

<template>
  <div class="mx-auto w-100 max-w-6xl px-3 pb-5 pt-5 px-sm-4 pt-sm-5">
    <header class="pb-5">
      <p class="font-mono text-xs text-uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
      <h1 class="mt-3 font-display text-3xl fw-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("nav.watchlist") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("watch.subtitle") }}</p>
    </header>

    <p v-if="msg" class="mb-3 font-mono text-sm text-down">{{ msg }}</p>

    <form class="mb-5 d-flex flex-column gap-3 rounded-4 border border-rule bg-paper-2 p-4 flex-sm-row align-items-sm-end" @submit.prevent="addEntry">
      <label class="d-flex flex-column gap-1.5 sm:max-w-[14rem]">
        <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("watch.addTicker") }}</span>
        <Input v-model="addTicker" list="stock-tickers" :placeholder="t('watch.tickerPlaceholder')" required />
        <datalist id="stock-tickers">
          <option v-for="s in stocks" :key="s.ticker" :value="s.ticker">{{ s.company_name }}</option>
        </datalist>
      </label>
      <label class="d-flex flex-column gap-1.5">
        <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("watch.addTarget") }}</span>
        <Input v-model="addTarget" type="number" min="0" step="0.01" :placeholder="t('watch.optional')" />
      </label>
      <Button :disabled="busy" class="sm:mb-0.5">{{ t("watch.addButton") }}</Button>
    </form>

    <p v-if="entries.length === 0" class="text-muted">{{ t("watch.empty") }}</p>
    <table v-else class="w-100 border-collapse text-sm">
      <thead>
        <tr class="border-bottom border-rule text-start font-mono text-xs text-uppercase tracking-[0.2em] text-muted">
          <th class="py-3 pe-3">{{ t("market.ticker") }}</th>
          <th class="d-none py-3 pe-3 d-md-table-cell">{{ t("market.company") }}</th>
          <th class="py-3 pe-3 text-end">{{ t("watch.current") }}</th>
          <th class="py-3 pe-3 text-end">{{ t("watch.target") }}</th>
          <th class="d-none py-3 pe-3 text-end d-lg-table-cell">{{ t("watch.gap") }}</th>
          <th class="d-none py-3 pe-3 d-md-table-cell">{{ t("watch.added") }}</th>
          <th class="py-3 text-end"><span class="sr-only">Remove</span></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="e in entries" :key="e.watchlist_id" class="border-bottom border-rule">
          <td class="py-3 pe-3">
            <RouterLink :to="`/stocks/${e.ticker}`" class="font-mono fw-semibold text-ink hover:text-band">{{ e.ticker }}</RouterLink>
          </td>
          <td class="d-none py-3 pe-3 text-muted d-md-table-cell">{{ e.company_name }}</td>
          <td class="py-3 pe-3 text-end font-mono">{{ fmtPrice(currentOf(e)) }}</td>
          <td class="py-3 pe-3 text-end">
            <span class="d-inline-flex align-items-center gap-2">
              <input
                :value="fmtTarget(e)"
                type="number"
                min="0"
                step="0.01"
                class="w-24 rounded-3 border border-rule bg-paper-2 px-2 py-1 font-mono text-xs text-ink transition-colors duration-150 hover:border-muted/60 focus-visible:outline-2 focus-visible:outline-offset-0 focus-visible:outline-focus"
                @change="setTarget(e, $event)"
              />
            </span>
          </td>
          <td class="d-none py-3 pe-3 text-end font-mono d-lg-table-cell" :class="dirClass(distance(e))">
            {{ signed((distance(e) ?? 0) / 1000) }}
          </td>
          <td class="d-none py-3 pe-3 font-mono text-xs text-muted d-md-table-cell">{{ fmtShortDate(e.created_at) }}</td>
          <td class="py-3 text-end">
            <button
              type="button"
              class="rounded-pill border border-rule px-3 py-1 font-mono text-xs text-muted transition-colors hover:border-down hover:text-down"
              @click="remove(e)"
            >
              {{ t("stock.removeWatch") }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
