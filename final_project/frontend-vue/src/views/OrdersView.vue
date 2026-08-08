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
  <div class="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
    <header class="pb-10">
      <p class="font-mono text-xs uppercase tracking-[0.25em] text-muted">{{ t("brand.name") }}</p>
      <h1 class="mt-3 font-display text-3xl font-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("nav.orders") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("orders.subtitle") }}</p>
    </header>

    <p v-if="error" class="mb-4 font-mono text-sm text-down">{{ error }}</p>
    <p v-if="orders.length === 0" class="text-muted">{{ t("orders.empty") }}</p>
    <table v-else class="w-full border-collapse text-sm">
      <thead>
        <tr class="border-b border-rule text-left font-mono text-xs uppercase tracking-[0.2em] text-muted">
          <th class="py-3 pr-4">{{ t("orders.id") }}</th>
          <th class="py-3 pr-4">{{ t("portfolio.type") }}</th>
          <th class="hidden py-3 pr-4 sm:table-cell">{{ t("orders.style") }}</th>
          <th class="py-3 pr-4 text-right">{{ t("portfolio.qty") }}</th>
          <th class="hidden py-3 pr-4 text-right sm:table-cell">{{ t("orders.limit") }}</th>
          <th class="py-3 pr-4">{{ t("orders.status") }}</th>
          <th class="py-3 text-right">{{ t("portfolio.date") }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="o in orders" :key="o.order_id" class="border-b border-rule">
          <td class="py-3 pr-4 font-mono text-xs text-muted">{{ o.order_id.slice(0, 8) }}</td>
          <td class="py-3 pr-4"><Badge>{{ o.order_type }}</Badge></td>
          <td class="hidden py-3 pr-4 sm:table-cell">{{ o.order_style }}</td>
          <td class="py-3 pr-4 text-right font-mono">{{ fmtQty(o.quantity) }}</td>
          <td class="hidden py-3 pr-4 text-right font-mono sm:table-cell">{{ fmtPrice(o.limit_price) }}</td>
          <td class="py-3 pr-4">
            <Badge :variant="STATUS_VARIANT[o.status] ?? 'neutral'">{{ o.status }}</Badge>
          </td>
          <td class="py-3 text-right font-mono text-xs text-muted">{{ fmtDate(o.created_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
