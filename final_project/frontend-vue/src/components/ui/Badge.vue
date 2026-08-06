<script setup lang="ts">
import { computed } from "vue";

type Variant = "neutral" | "accent";

const props = withDefaults(defineProps<{ variant?: Variant }>(), { variant: "neutral" });

const classes = computed(() => {
  const variants: Record<Variant, string> = {
    neutral: "border-border bg-surface text-muted",
    accent: "border-accent/40 bg-accent-soft text-accent-hover",
  };
  return (
    "inline-flex items-center whitespace-nowrap rounded-full border px-2.5 py-0.5 font-mono text-xs font-medium tracking-wide " +
    variants[props.variant]
  );
});
</script>

<template>
  <span :class="classes"><slot /></span>
</template>
