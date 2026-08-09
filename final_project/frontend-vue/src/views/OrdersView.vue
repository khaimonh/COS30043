<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useI18n } from "../i18n";
import Badge from "../components/ui/Badge.vue";
import { api } from "../lib/api";
import { fmtQty, fmtPrice, fmtDate } from "../lib/format";
import type { Order } from "../lib/types";

const { t } = useI18n();

const orders = ref<Order[]>([]);
const error = ref("");

const STATUS_VARIANT: Record<string, "neutral" | "accent"> = {
  Filled: "accent",
  Pending: "neutral",
  Rejected: "neutral",
  Cancelled: "neutral",
};

onMounted(async () => {
  try {
    orders.value = await api<Order[]>("/orders");
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Error";
  }
});
</script>

<template>
  <div class="mx-auto w-100 max-w-6xl px-3 pb-5 pt-5 px-sm-4 pt-sm-5">
    <header class="pb-5">
      <p class="font-mono text-xs text-uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
      <h1 class="mt-3 font-display text-3xl fw-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("nav.orders") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("orders.subtitle") }}</p>
    </header>

    <p v-if="error" class="mb-3 font-mono text-sm text-down">{{ error }}</p>
    <p v-if="orders.length === 0" class="text-muted">{{ t("orders.empty") }}</p>
    <table v-else class="w-100 border-collapse text-sm">
      <thead>
        <tr class="border-bottom border-rule text-start font-mono text-xs text-uppercase tracking-[0.2em] text-muted">
          <th class="py-3 pe-3">{{ t("orders.id") }}</th>
          <th class="py-3 pe-3">{{ t("portfolio.type") }}</th>
          <th class="d-none py-3 pe-3 d-sm-table-cell">{{ t("orders.style") }}</th>
          <th class="py-3 pe-3 text-end">{{ t("portfolio.qty") }}</th>
          <th class="d-none py-3 pe-3 text-end d-sm-table-cell">{{ t("orders.limit") }}</th>
          <th class="py-3 pe-3">{{ t("orders.status") }}</th>
          <th class="py-3 text-end">{{ t("portfolio.date") }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="o in orders" :key="o.order_id" class="border-bottom border-rule">
          <td class="py-3 pe-3 font-mono text-xs text-muted">{{ o.order_id.slice(0, 8) }}</td>
          <td class="py-3 pe-3"><Badge>{{ o.order_type }}</Badge></td>
          <td class="d-none py-3 pe-3 d-sm-table-cell">{{ o.order_style }}</td>
          <td class="py-3 pe-3 text-end font-mono">{{ fmtQty(o.quantity) }}</td>
          <td class="d-none py-3 pe-3 text-end font-mono d-sm-table-cell">{{ fmtPrice(o.limit_price) }}</td>
          <td class="py-3 pe-3">
            <Badge :variant="STATUS_VARIANT[o.status] ?? 'neutral'">{{ o.status }}</Badge>
          </td>
          <td class="py-3 text-end font-mono text-xs text-muted">{{ fmtDate(o.created_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
