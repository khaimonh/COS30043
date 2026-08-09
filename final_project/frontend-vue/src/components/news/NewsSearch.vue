<script setup lang="ts">
import { useI18n } from "../../i18n";
import Input from "../ui/Input.vue";
import Select from "../ui/Select.vue";

const { t } = useI18n();

defineProps<{
  query: string;
  category: string;
  categories: string[];
}>();

const emit = defineEmits<{
  (e: "update:query", value: string): void;
  (e: "update:category", value: string): void;
}>();
</script>

<template>
  <div class="row g-3">
    <Input
      class="col"
      type="search"
      :model-value="query"
      :aria-label="t('news.searchPlaceholder')"
      :placeholder="t('news.searchPlaceholder')"
      @update:model-value="emit('update:query', String($event))"
    />
    <Select
      class="col-12 col-sm-auto"
      :model-value="category"
      :aria-label="t('news.allCategories')"
      @update:model-value="emit('update:category', String($event))"
    >
      <option value="">{{ t("news.allCategories") }}</option>
      <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
    </Select>
  </div>
</template>
