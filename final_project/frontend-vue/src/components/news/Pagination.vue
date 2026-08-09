<script setup lang="ts">
import { useI18n } from "../../i18n";
import Button from "../ui/Button.vue";

const { t, tf } = useI18n();

defineProps<{ page: number; totalPages: number }>();
const emit = defineEmits<{ (e: "page", value: number): void }>();
</script>

<template>
  <nav
    v-if="totalPages > 1"
    class="d-flex align-items-center justify-content-between gap-4 border-top border-rule pt-3"
    aria-label="pagination"
  >
    <Button variant="ghost" size="sm" :disabled="page <= 1" @click="emit('page', page - 1)">
      {{ t("news.prev") }}
    </Button>
    <span class="font-mono text-xs text-muted">
      {{ tf("news.pageOf", { page: String(page), total: String(totalPages) }) }}
    </span>
    <Button variant="ghost" size="sm" :disabled="page >= totalPages" @click="emit('page', page + 1)">
      {{ t("news.next") }}
    </Button>
  </nav>
</template>
