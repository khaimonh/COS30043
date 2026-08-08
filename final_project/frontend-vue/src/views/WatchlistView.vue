<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useI18n } from "../i18n";
import Button from "../components/ui/Button.vue";
import Input from "../components/ui/Input.vue";
import { api } from "../lib/api";
import { fmtPrice, fmtShortDate, signed, dirClass, num } from "../lib/format";
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
  } catch (e) {
    msg.value = e instanceof Error ? e.message : "Error";
  }
}

async function loadStocks() {
  try {
    stocks.value = await api<Stock[]>("/stocks");
  } catch {
    /* ignore */
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

function distance(entry: WatchlistEntry): number | null {
  const cur = num(entry.current_price);
  const target = num(entry.target_price);
  if (cur === null || target === null) return null;
  return cur - target;
}

onMounted(async () => {
  await loadStocks();
  await load();
});
</script>

<template>
  <div class="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
    <header class="pb-10">
      <p class="font-mono text-xs uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
      <h1 class="mt-3 font-display text-3xl font-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("nav.watchlist") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("watch.subtitle") }}</p>
    </header>

    <p v-if="msg" class="mb-4 font-mono text-sm text-down">{{ msg }}</p>

    <form class="mb-8 flex flex-col gap-3 rounded-2xl border border-rule bg-paper-2 p-6 sm:flex-row sm:items-end" @submit.prevent="addEntry">
      <label class="flex flex-col gap-1.5 sm:max-w-[14rem]">
        <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">{{ t("watch.addTicker") }}</span>
        <Input v-model="addTicker" list="stock-tickers" :placeholder="t('watch.tickerPlaceholder')" required />
        <datalist id="stock-tickers">
          <option v-for="s in stocks" :key="s.ticker" :value="s.ticker">{{ s.company_name }}</option>
        </datalist>
      </label>
      <label class="flex flex-col gap-1.5">
        <span class="font-mono text-xs uppercase tracking-[0.2em] text-muted">{{ t("watch.addTarget") }}</span>
        <Input v-model="addTarget" type="number" min="0" step="0.01" :placeholder="t('watch.optional')" />
      </label>
      <Button :disabled="busy" class="sm:mb-0.5">{{ t("watch.addButton") }}</Button>
    </form>

    <p v-if="entries.length === 0" class="text-muted">{{ t("watch.empty") }}</p>
    <table v-else class="w-full border-collapse text-sm">
      <thead>
        <tr class="border-b border-rule text-left font-mono text-xs uppercase tracking-[0.2em] text-muted">
          <th class="py-3 pr-4">{{ t("market.ticker") }}</th>
          <th class="hidden py-3 pr-4 md:table-cell">{{ t("market.company") }}</th>
          <th class="py-3 pr-4 text-right">{{ t("watch.current") }}</th>
          <th class="py-3 pr-4 text-right">{{ t("watch.target") }}</th>
          <th class="hidden py-3 pr-4 text-right lg:table-cell">{{ t("watch.gap") }}</th>
          <th class="hidden py-3 pr-4 md:table-cell">{{ t("watch.added") }}</th>
          <th class="py-3 text-right"><span class="sr-only">Remove</span></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="e in entries" :key="e.watchlist_id" class="border-b border-rule">
          <td class="py-3 pr-4">
            <RouterLink :to="`/stocks/${e.ticker}`" class="font-mono font-semibold text-ink hover:text-band">{{ e.ticker }}</RouterLink>
          </td>
          <td class="hidden py-3 pr-4 text-muted md:table-cell">{{ e.company_name }}</td>
          <td class="py-3 pr-4 text-right font-mono">{{ fmtPrice(e.current_price) }}</td>
          <td class="py-3 pr-4 text-right">
            <span class="inline-flex items-center gap-2">
              <input
                :value="fmtTarget(e)"
                type="number"
                min="0"
                step="0.01"
                class="w-24 rounded-lg border border-rule bg-paper-2 px-2 py-1 font-mono text-xs text-ink transition-colors duration-150 hover:border-muted/60 focus-visible:outline-2 focus-visible:outline-offset-0 focus-visible:outline-focus"
                @change="setTarget(e, $event)"
              />
            </span>
          </td>
          <td class="hidden py-3 pr-4 text-right font-mono lg:table-cell" :class="dirClass(distance(e))">
            {{ signed((distance(e) ?? 0) / 1000) }}
          </td>
          <td class="hidden py-3 pr-4 font-mono text-xs text-muted md:table-cell">{{ fmtShortDate(e.created_at) }}</td>
          <td class="py-3 text-right">
            <button
              type="button"
              class="rounded-full border border-rule px-3 py-1 font-mono text-xs text-muted transition-colors hover:border-down hover:text-down"
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
