<script setup lang="ts">
import type { NewsItem } from "../../lib/news";
import { fmtShortDate } from "../../lib/format";
import Badge from "../ui/Badge.vue";

defineProps<{ item: NewsItem }>();
</script>

<template>
  <article class="py-3">
    <div class="d-flex flex-wrap align-items-baseline gap-x-3 gap-y-1">
      <time class="font-mono text-xs text-muted" :datetime="item.date">
        {{ fmtShortDate(item.date) }}
      </time>
      <Badge>{{ item.category }}</Badge>
    </div>
    <h3 class="mt-2.5 text-lg fw-semibold leading-snug tracking-tight text-ink">
      {{ item.title }}
    </h3>
    <p class="mt-2 max-w-[70ch] text-sm leading-relaxed text-muted">
      {{ item.content }}
    </p>
  </article>
</template>
