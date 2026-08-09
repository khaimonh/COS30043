<script setup lang="ts">
import { computed } from "vue";

type Size = "sm" | "md" | "lg";

const props = withDefaults(defineProps<{ size?: Size }>(), { size: "md" });

const tile = computed(() => (props.size === "sm" ? "h-7 w-7" : props.size === "lg" ? "h-12 w-12" : "h-9 w-9"));
const svg = computed(() => (props.size === "sm" ? "h-4 w-4" : props.size === "lg" ? "h-6 w-6" : "h-5 w-5"));
</script>

<template>
  <span class="d-flex align-items-center justify-content-center rounded-pill bg-band" :class="tile">
    <svg :class="svg" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 3 L21 12 L12 21 L3 12 Z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round" class="text-band-ink" />
      <circle cx="12" cy="12" r="2.6" fill="currentColor" class="text-band-ink" />
    </svg>
  </span>
</template>
