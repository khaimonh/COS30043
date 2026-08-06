<script setup lang="ts">
import { computed, ref } from "vue";
import { useI18n } from "../i18n";
import NewsList from "../components/news/NewsList.vue";
import NewsSearch from "../components/news/NewsSearch.vue";
import Pagination from "../components/news/Pagination.vue";
import { matchesSearch, PAGE_SIZE, type NewsItem } from "../lib/news";

const { t, tf } = useI18n();

const items = ref<NewsItem[] | null>(null);
const query = ref("");
const category = ref("");
const page = ref(1);

fetch("/data/news.json")
  .then((res) => res.json())
  .then((data) => (items.value = data.items))
  .catch(() => (items.value = []));

const categories = computed(() => [...new Set((items.value ?? []).map((i) => i.category))]);

const filtered = computed(() =>
  (items.value ?? []).filter(
    (item) =>
      matchesSearch(item, query.value) &&
      (category.value === "" || item.category === category.value)
  )
);

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / PAGE_SIZE)));
const current = computed(() => Math.min(page.value, totalPages.value));
const visible = computed(() =>
  filtered.value.slice((current.value - 1) * PAGE_SIZE, current.value * PAGE_SIZE)
);
</script>

<template>
  <div class="mx-auto w-full max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-14">
    <header class="pb-10">
      <p class="font-mono text-xs uppercase tracking-[0.25em] text-muted">
        {{ t("brand.name") }}
      </p>
      <h1 class="mt-3 font-display text-3xl font-bold tracking-[-0.02em] text-ink sm:text-4xl">
        {{ t("news.title") }}
      </h1>
      <p class="mt-3 max-w-[65ch] text-muted">{{ t("news.subtitle") }}</p>
      <p class="mt-1.5 font-mono text-[11px] tracking-[0.15em] text-muted/70">{{ t("news.demoNote") }}</p>
    </header>

    <div class="mb-8 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="max-w-xl flex-1">
        <NewsSearch
          :query="query"
          :category="category"
          :categories="categories"
          @update:query="(v: string) => { query = v; page = 1; }"
          @update:category="(v: string) => { category = v; page = 1; }"
        />
      </div>
      <p class="font-mono text-xs text-muted">
        {{ tf("news.results", { n: String(filtered.length) }) }}
      </p>
    </div>

    <p v-if="items === null" class="text-muted">{{ t("news.loading") }}</p>
    <p v-else-if="visible.length === 0" class="text-muted">{{ t("news.empty") }}</p>
    <template v-else>
      <NewsList :items="visible" />
      <div class="mt-10">
        <Pagination :page="current" :total-pages="totalPages" @page="(p: number) => (page = p)" />
      </div>
    </template>
  </div>
</template>
