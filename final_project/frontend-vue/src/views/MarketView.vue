<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "../i18n";
import { api } from "../lib/api";
import { token } from "../lib/session";
import { fmtPrice, num, signed, dirClass } from "../lib/format";
import type { Stock, Quote } from "../lib/types";

const { t } = useI18n();
const router = useRouter();

const stocks = ref<Stock[]>([]);
const quotes = ref<Record<string, Quote | null>>({});
const query = ref("");
const loading = ref(true);
const error = ref("");
const watched = ref<Set<string>>(new Set());
const watchMsg = ref("");

const POLL_MS = 15_000;
let pollTimer: number | undefined;

async function loadStocks() {
  try {
    stocks.value = await api<Stock[]>("/stocks");
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  } finally {
    loading.value = false;
  }
}

async function loadQuotes() {
  try {
    quotes.value = await api<Record<string, Quote | null>>("/stocks/quotes");
  } catch {
    /* stale quotes are fine */
  }
}

async function loadWatchlist() {
  if (!token.value) return;
  try {
    const list = await api<{ ticker: string }[]>("/watchlist");
    watched.value = new Set(list.map((w) => w.ticker));
  } catch {
    /* ignore */
  }
}

async function toggleWatch(ticker: string) {
  watchMsg.value = "";
  try {
    if (watched.value.has(ticker)) {
      const list = await api<{ ticker: string; watchlist_id: string }[]>("/watchlist");
      const entry = list.find((w) => w.ticker === ticker);
      if (entry) await api(`/watchlist/${entry.watchlist_id}`, { method: "DELETE" });
      watched.value.delete(ticker);
    } else {
      await api("/watchlist", { body: { ticker } });
      watched.value.add(ticker);
    }
  } catch (e) {
    watchMsg.value = e instanceof Error ? e.message : "Error";
  }
}

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase();
  if (!q) return stocks.value;
  return stocks.value.filter(
    (s) => s.ticker.toLowerCase().includes(q) || s.company_name.toLowerCase().includes(q)
  );
});

function changeOf(ticker: string): number | null {
  const q = quotes.value[ticker];
  if (!q) return null;
  return num(q.change ?? q.change_price ?? q.pct_change);
}

onMounted(() => {
  loadStocks();
  loadQuotes();
  loadWatchlist();
  pollTimer = window.setInterval(loadQuotes, POLL_MS);
});

onBeforeUnmount(() => window.clearInterval(pollTimer));
</script>

<template>
  <div class="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
    <header class="pb-10">
      <p class="font-mono text-xs uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
      <h1 class="mt-3 font-display text-3xl font-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("market.title") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("market.subtitle") }}</p>
    </header>

    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <input
        v-model="query"
        class="w-full max-w-xl rounded-lg border border-rule bg-paper-2 px-3.5 py-2 text-sm text-ink placeholder:text-muted transition-colors duration-150 hover:border-muted/60 focus-visible:outline-2 focus-visible:outline-offset-0 focus-visible:outline-focus"
        :placeholder="t('market.search')"
        type="search"
      />
      <p class="font-mono text-xs text-muted">{{ t("market.liveNote") }}</p>
    </div>

    <p v-if="error" class="mb-4 font-mono text-sm text-down">{{ error }}</p>
    <p v-if="watchMsg" class="mb-4 font-mono text-sm text-down">{{ watchMsg }}</p>
    <p v-if="loading" class="text-muted">{{ t("news.loading") }}</p>
    <p v-else-if="filtered.length === 0" class="text-muted">{{ t("market.empty") }}</p>
    <table v-else class="w-full border-collapse text-sm">
      <thead>
        <tr class="border-b border-rule text-left font-mono text-xs uppercase tracking-[0.2em] text-muted">
          <th class="py-3 pr-4">{{ t("market.ticker") }}</th>
          <th class="py-3 pr-4">{{ t("market.company") }}</th>
          <th class="hidden py-3 pr-4 md:table-cell">{{ t("market.exchange") }}</th>
          <th class="hidden py-3 pr-4 lg:table-cell">{{ t("market.sector") }}</th>
          <th class="py-3 pr-4 text-right">{{ t("market.price") }}</th>
          <th class="py-3 pr-4 text-right">{{ t("market.change") }}</th>
          <th class="py-3 text-right"><span class="sr-only">Watch</span></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="s in filtered"
          :key="s.ticker"
          class="cursor-pointer border-b border-rule transition-colors hover:bg-paper-2"
          @click="router.push(`/stocks/${s.ticker}`)"
        >
          <td class="py-3 pr-4 font-mono font-semibold tracking-wide text-ink">{{ s.ticker }}</td>
          <td class="py-3 pr-4 text-muted">{{ s.company_name }}</td>
          <td class="hidden py-3 pr-4 font-mono text-xs text-muted md:table-cell">{{ s.exchange }}</td>
          <td class="hidden py-3 pr-4 text-xs text-muted lg:table-cell">{{ s.sector }}</td>
          <td class="py-3 pr-4 font-mono tabular-nums">{{ fmtPrice(quotes[s.ticker]?.close_price) }}</td>
          <td class="py-3 pr-4 text-right font-mono tabular-nums" :class="dirClass(changeOf(s.ticker))">
            {{ signed(changeOf(s.ticker)) }}
          </td>
          <td class="py-3 text-right">
            <button
              v-if="token"
              type="button"
              class="rounded-full border px-3 py-1 font-mono text-xs transition-colors duration-150"
              :class="
                watched.has(s.ticker)
                  ? 'border-band bg-band text-band-ink'
                  : 'border-rule text-muted hover:text-ink'
              "
              :aria-label="s.ticker"
              @click.stop="toggleWatch(s.ticker)"
            >
              {{ watched.has(s.ticker) ? t("market.remove") : t("market.add") }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
