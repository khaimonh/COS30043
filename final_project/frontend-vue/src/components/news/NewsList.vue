<script setup lang="ts">
import type { NewsItem } from "../../lib/news";
import NewsCard from "./NewsCard.vue";

defineProps<{ items: NewsItem[] }>();
</script>

<template>
  <div class="divide-y divide-rule">
    <NewsCard v-for="item in items" :key="item.id" :item="item" />
  </div>
</template>
