<script setup lang="ts">
defineProps<{ modelValue?: string | number }>();
defineEmits<{ (e: "update:modelValue", value: string): void }>();
</script>

<template>
  <input
    class="w-100 rounded-3 border border-rule bg-paper-2 px-3.5 py-2 text-sm text-ink placeholder:text-muted transition-colors duration-150 hover:border-muted/60 focus-visible:outline-2 focus-visible:outline-offset-0 focus-visible:outline-focus"
    :value="modelValue"
    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
  />
</template>
