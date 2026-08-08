<script setup lang="ts">
import { computed } from "vue";

type Variant = "primary" | "outline" | "ghost";
type Size = "sm" | "md" | "lg";

const props = withDefaults(
  defineProps<{ variant?: Variant; size?: Size; type?: "button" | "submit" }>(),
  { variant: "primary", size: "md", type: "submit" }
);

const classes = computed(() => {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-full font-medium " +
    "transition-[color,background-color,border-color,transform] duration-150 ease-out " +
    "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus " +
    "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-55 active:scale-[0.98]";
  const variants: Record<Variant, string> = {
    primary: "bg-band text-band-ink hover:bg-band-2",
    outline: "border border-ink text-ink hover:bg-ink hover:text-paper",
    ghost: "text-muted hover:text-ink",
  };
  const sizes: Record<Size, string> = {
    sm: "px-4 py-2 text-sm",
    md: "px-5 py-2.5 text-sm",
    lg: "px-7 py-3.5 text-base",
  };
  return [base, variants[props.variant], sizes[props.size]].join(" ");
});
</script>

<template>
  <button :type="type" :class="classes"><slot /></button>
</template>
