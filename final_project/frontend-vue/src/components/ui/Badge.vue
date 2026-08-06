<script setup lang="ts">
import { computed } from "vue";

type Variant = "neutral" | "accent";

const props = withDefaults(defineProps<{ variant?: Variant }>(), { variant: "neutral" });

const classes = computed(() => {
  const variants: Record<Variant, string> = {
    neutral: "border-rule bg-paper-2 text-muted",
    accent: "border-band bg-band text-band-ink",
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
