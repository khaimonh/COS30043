<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useI18n } from "../i18n";
import Badge from "../components/ui/Badge.vue";
import Button from "../components/ui/Button.vue";
import { api } from "../lib/api";
import { fmtQty, fmtPrice, fmtDate, fmtShortDate } from "../lib/format";

const { t } = useI18n();

type AdminUser = {
  user_id: string;
  email: string;
  full_name: string;
  role: string;
  status: string;
  created_at: string | null;
};

type AdminOrder = {
  order_id: string;
  user_email: string;
  ticker: string;
  order_type: string;
  order_style: string;
  status: string;
  quantity: number;
  limit_price: string | null;
  created_at: string | null;
};

type AdminTrade = {
  trade_id: string;
  order_id: string;
  user_email: string;
  ticker: string;
  execution_price: string;
  executed_quantity: number;
  executed_at: string | null;
};

type Health = {
  queues: { status: string; queue_depth: number | null; dlq_depth: number | null };
  order_counts: Record<string, number>;
};

const tab = ref<"users" | "orders" | "trades" | "health">("users");
const users = ref<AdminUser[]>([]);
const orders = ref<AdminOrder[]>([]);
const trades = ref<AdminTrade[]>([]);
const health = ref<Health | null>(null);
const error = ref("");

async function loadUsers() {
  try {
    users.value = await api<AdminUser[]>("/admin/users");
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  }
}
async function loadOrders() {
  try {
    orders.value = await api<AdminOrder[]>("/admin/orders");
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  }
}
async function loadTrades() {
  try {
    trades.value = await api<AdminTrade[]>("/admin/trades");
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  }
}
async function loadHealth() {
  try {
    health.value = await api<Health>("/admin/health");
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  }
}

async function toggleUser(u: AdminUser) {
  error.value = "";
  try {
    const next = u.status === "Active" ? "Suspended" : "Active";
    await api(`/admin/users/${u.user_id}/status`, { method: "PATCH", body: { status: next } });
    await loadUsers();
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  }
}

const TABS = [
  { key: "users", label: () => t("admin.users") },
  { key: "orders", label: () => t("admin.orders") },
  { key: "trades", label: () => t("admin.trades") },
  { key: "health", label: () => t("admin.health") },
] as const;

function switchTab(k: typeof tab.value) {
  tab.value = k;
  if (k === "users" && users.value.length === 0) loadUsers();
  if (k === "orders" && orders.value.length === 0) loadOrders();
  if (k === "trades" && trades.value.length === 0) loadTrades();
  if (k === "health" && !health.value) loadHealth();
}

onMounted(() => loadUsers());
</script>

<template>
  <div class="mx-auto w-100 max-w-6xl px-3 pb-5 pt-5 px-sm-4 pt-sm-5">
    <header class="pb-5">
      <p class="font-mono text-xs text-uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
      <h1 class="mt-3 font-display text-3xl fw-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("nav.admin") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("admin.subtitle") }}</p>
    </header>

    <div class="mb-5 d-flex flex-wrap gap-2">
      <button
        v-for="tb in TABS"
        :key="tb.key"
        type="button"
        class="rounded-pill border px-3 py-2 font-mono text-sm transition-colors duration-150"
        :class="tab === tb.key ? 'border-band bg-band text-band-ink' : 'border-rule text-muted hover:text-ink'"
        @click="switchTab(tb.key)"
      >
        {{ tb.label() }}
      </button>
    </div>

    <p v-if="error" class="mb-3 font-mono text-sm text-down">{{ error }}</p>

    <section v-if="tab === 'users'" class="rounded-4 border border-rule bg-paper-2 p-4">
      <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("admin.users") }}</h2>
      <table class="mt-3 w-100 border-collapse text-sm">
        <thead>
          <tr class="border-bottom border-rule text-start font-mono text-xs text-uppercase tracking-[0.2em] text-muted">
            <th class="py-2 pe-3">{{ t("admin.email") }}</th>
            <th class="d-none py-2 pe-3 d-sm-table-cell">{{ t("admin.name") }}</th>
            <th class="py-2 pe-3">{{ t("admin.role") }}</th>
            <th class="py-2 pe-3">{{ t("admin.status") }}</th>
            <th class="d-none py-2 pe-3 d-md-table-cell">{{ t("admin.created") }}</th>
            <th class="py-2 text-end"><span class="sr-only">Toggle</span></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.user_id" class="border-bottom border-rule">
            <td class="py-2 pe-3 fw-medium text-ink">{{ u.email }}</td>
            <td class="d-none py-2 pe-3 text-muted d-sm-table-cell">{{ u.full_name }}</td>
            <td class="py-2 pe-3"><Badge :variant="u.role === 'Admin' ? 'accent' : 'neutral'">{{ u.role }}</Badge></td>
            <td class="py-2 pe-3"><Badge>{{ u.status }}</Badge></td>
            <td class="d-none py-2 pe-3 font-mono text-xs text-muted d-md-table-cell">{{ fmtShortDate(u.created_at) }}</td>
            <td class="py-2 text-end">
              <Button v-if="u.role !== 'Admin'" variant="ghost" size="sm" @click="toggleUser(u)">
                {{ u.status === "Active" ? t("admin.suspend") : t("admin.activate") }}
              </Button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <section v-if="tab === 'orders'" class="rounded-4 border border-rule bg-paper-2 p-4">
      <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("admin.orders") }}</h2>
      <p v-if="orders.length === 0" class="mt-3 text-sm text-muted">{{ t("orders.empty") }}</p>
      <table v-else class="mt-3 w-100 border-collapse text-sm">
        <thead>
          <tr class="border-bottom border-rule text-start font-mono text-xs text-uppercase tracking-[0.2em] text-muted">
            <th class="py-2 pe-3">{{ t("admin.email") }}</th>
            <th class="py-2 pe-3">{{ t("market.ticker") }}</th>
            <th class="py-2 pe-3">{{ t("portfolio.type") }}</th>
            <th class="d-none py-2 pe-3 d-sm-table-cell">{{ t("orders.style") }}</th>
            <th class="py-2 pe-3 text-end">{{ t("portfolio.qty") }}</th>
            <th class="py-2 pe-3">{{ t("orders.status") }}</th>
            <th class="py-2 text-end">{{ t("portfolio.date") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="o in orders" :key="o.order_id" class="border-bottom border-rule">
            <td class="py-2 pe-3 text-muted">{{ o.user_email }}</td>
            <td class="py-2 pe-3 font-mono fw-semibold text-ink">{{ o.ticker }}</td>
            <td class="py-2 pe-3"><Badge>{{ o.order_type }}</Badge></td>
            <td class="d-none py-2 pe-3 d-sm-table-cell">{{ o.order_style }}</td>
            <td class="py-2 pe-3 text-end font-mono">{{ fmtQty(o.quantity) }}</td>
            <td class="py-2 pe-3"><Badge>{{ o.status }}</Badge></td>
            <td class="py-2 text-end font-mono text-xs text-muted">{{ fmtDate(o.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section v-if="tab === 'trades'" class="rounded-4 border border-rule bg-paper-2 p-4">
      <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("admin.trades") }}</h2>
      <p v-if="trades.length === 0" class="mt-3 text-sm text-muted">{{ t("trades.empty") }}</p>
      <table v-else class="mt-3 w-100 border-collapse text-sm">
        <thead>
          <tr class="border-bottom border-rule text-start font-mono text-xs text-uppercase tracking-[0.2em] text-muted">
            <th class="py-2 pe-3">{{ t("admin.email") }}</th>
            <th class="py-2 pe-3">{{ t("market.ticker") }}</th>
            <th class="py-2 pe-3 text-end">{{ t("orders.price") }}</th>
            <th class="py-2 pe-3 text-end">{{ t("portfolio.qty") }}</th>
            <th class="py-2 text-end">{{ t("portfolio.date") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tr in trades" :key="tr.trade_id" class="border-bottom border-rule">
            <td class="py-2 pe-3 text-muted">{{ tr.user_email }}</td>
            <td class="py-2 pe-3 font-mono fw-semibold text-ink">{{ tr.ticker }}</td>
            <td class="py-2 pe-3 text-end font-mono">{{ fmtPrice(tr.execution_price) }}</td>
            <td class="py-2 pe-3 text-end font-mono">{{ fmtQty(tr.executed_quantity) }}</td>
            <td class="py-2 text-end font-mono text-xs text-muted">{{ fmtDate(tr.executed_at) }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section v-if="tab === 'health'" class="row row-cols-1 row-cols-sm-2 g-4">
      <div class="rounded-4 border border-rule bg-paper-2 p-4">
        <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("admin.queues") }}</h2>
        <p v-if="!health" class="mt-3 text-sm text-muted">{{ t("news.loading") }}</p>
        <template v-else>
          <div class="mt-3 d-flex flex-column gap-3">
            <div class="d-flex align-items-center justify-content-between">
              <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("admin.queueStatus") }}</span>
              <Badge :variant="health.queues.status === 'up' ? 'accent' : 'neutral'">{{ health.queues.status }}</Badge>
            </div>
            <div class="d-flex align-items-center justify-content-between">
              <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("admin.queueDepth") }}</span>
              <span class="font-mono text-sm text-ink">{{ health.queues.queue_depth ?? "—" }}</span>
            </div>
            <div class="d-flex align-items-center justify-content-between">
              <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ t("admin.dlq") }}</span>
              <span class="font-mono text-sm text-ink">{{ health.queues.dlq_depth ?? "—" }}</span>
            </div>
          </div>
        </template>
      </div>
      <div class="rounded-4 border border-rule bg-paper-2 p-4">
        <h2 class="font-display text-xl fw-bold tracking-[-0.02em] text-ink">{{ t("admin.orderCounts") }}</h2>
        <p v-if="!health" class="mt-3 text-sm text-muted">{{ t("news.loading") }}</p>
        <div v-else class="mt-3 d-flex flex-column gap-3">
          <div v-for="(count, status) in health.order_counts" :key="status" class="d-flex align-items-center justify-content-between">
            <span class="font-mono text-xs text-uppercase tracking-[0.2em] text-muted">{{ status }}</span>
            <span class="font-mono text-sm text-ink">{{ count }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
