<script setup lang="ts">
defineProps<{ modelValue?: string | number }>();
defineEmits<{ (e: "update:modelValue", value: string): void }>();
</script>

<template>
  <input
    class="w-full rounded-lg border border-border bg-surface px-3.5 py-2 text-sm text-foreground placeholder:text-muted transition-colors duration-150 hover:border-muted/50 focus-visible:outline-2 focus-visible:outline-offset-0 focus-visible:outline-focus"
    :value="modelValue"
    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
  />
</template>
