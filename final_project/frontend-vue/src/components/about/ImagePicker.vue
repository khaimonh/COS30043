<script setup lang="ts">
import { computed, ref } from "vue";
import { useI18n } from "../../i18n";

const { t } = useI18n();

const scenes = [
  { key: "mountain", src: "/images/mountain.svg", label: "about.mountain", alt: "about.mountainAlt" },
  { key: "ocean", src: "/images/ocean.svg", label: "about.ocean", alt: "about.oceanAlt" },
] as const;

const scene = ref<string>("mountain");
const selected = computed(() => scenes.find((s) => s.key === scene.value) ?? scenes[0]);
</script>

<template>
  <div>
    <div role="radiogroup" :aria-label="t('about.sceneTitle')">
      <label v-for="s in scenes" :key="s.key" class="cursor-pointer">
        <input
          v-model="scene"
          type="radio"
          name="scene"
          :value="s.key"
          class="peer sr-only"
        />
        <span class="mr-4 inline-block py-1 font-mono text-sm text-muted underline decoration-border decoration-1 underline-offset-8 transition-colors duration-150 hover:text-foreground peer-checked:text-foreground peer-checked:decoration-accent">
          {{ t(s.label) }}
        </span>
      </label>
    </div>
    <div class="mt-8">
      <img
        :src="selected.src"
        :alt="t(selected.alt)"
        class="w-full rounded-2xl border border-border"
      />
    </div>
  </div>
</template>
