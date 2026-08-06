<script setup lang="ts">
defineOptions({ inheritAttrs: false });

defineProps<{ modelValue?: string }>();
defineEmits<{ (e: "update:modelValue", value: string): void }>();
</script>

<template>
  <div class="relative">
    <select
      v-bind="$attrs"
      class="w-full appearance-none rounded-lg border border-rule bg-paper-2 px-3.5 py-2 pr-9 text-sm text-ink transition-colors duration-150 hover:border-muted/60 focus-visible:outline-2 focus-visible:outline-offset-0 focus-visible:outline-focus"
      :value="modelValue"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    >
      <slot />
    </select>
    <svg
      class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted"
      viewBox="0 0 20 20"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      aria-hidden="true"
    >
      <path d="M6 8l4 4 4-4" stroke-linecap="round" stroke-linejoin="round" />
    </svg>
  </div>
</template>
