<script setup lang="ts">
import { computed, ref } from "vue";
import { useI18n } from "../../i18n";
import type { Dict } from "../../i18n/en";

const { t, tf } = useI18n();

type SceneKey = "mountain" | "ocean";

const scenes: ReadonlyArray<{ key: SceneKey; src: string; label: keyof Dict; alt: keyof Dict; swatch: string }> = [
  {
    key: "mountain",
    src: "/images/mountain.svg",
    label: "about.mountain",
    alt: "about.mountainAlt",
    swatch: "#23306e",
  },
  {
    key: "ocean",
    src: "/images/ocean.svg",
    label: "about.ocean",
    alt: "about.oceanAlt",
    swatch: "#1a1510",
  },
];

const scene = ref<SceneKey>("mountain");
const selected = computed(() => scenes.find((s) => s.key === scene.value) ?? scenes[0]);

function pick(key: SceneKey): void {
  scene.value = key;
}
</script>

<template>
  <figure class="rounded-2xl border border-rule bg-paper-2 p-5">
    <div class="flex items-baseline justify-between gap-3">
      <p class="font-mono text-xs tracking-[0.25em] text-muted">
        {{ t("about.sceneEyebrow").toUpperCase() }}
      </p>
      <p class="font-mono text-[10px] tracking-[0.15em] text-muted/70">
        {{ tf("about.sceneCounter", { n: scenes.length }) }}
      </p>
    </div>

    <div
      role="radiogroup"
      :aria-label="t('about.sceneTitle')"
      class="mt-4 inline-flex w-full rounded-full border border-rule bg-paper p-1"
    >
      <label
        v-for="(s, i) in scenes"
        :key="s.key"
        class="relative flex-1 cursor-pointer"
      >
        <input
          v-model="scene"
          type="radio"
          name="scene"
          :value="s.key"
          class="peer sr-only"
        />
        <span
          class="flex items-center justify-center gap-2 rounded-full px-4 py-2 font-mono text-xs tracking-[0.18em] uppercase transition-colors duration-150 ease-out text-muted hover:text-ink peer-focus-visible:outline-2 peer-focus-visible:outline-offset-2 peer-focus-visible:outline-focus"
          :class="scene === s.key ? 'bg-band text-band-ink hover:text-band-ink' : ''"
          @click="pick(s.key)"
        >
          <span
            aria-hidden="true"
            class="inline-block h-1.5 w-1.5 rounded-full"
            :class="scene === s.key ? 'bg-band-ink' : ''"
            :style="{ backgroundColor: scene === s.key ? undefined : s.swatch }"
          />
          {{ t(s.label) }}
        </span>
        <span
          v-if="i < scenes.length - 1"
          aria-hidden="true"
          class="pointer-events-none absolute right-0 top-1/2 h-4 w-px -translate-y-1/2 bg-rule"
        />
      </label>
    </div>

    <div class="mt-5 overflow-hidden rounded-2xl border border-rule bg-paper">
      <Transition mode="out-in" name="scene-fade">
        <img
          :key="selected.key"
          :src="selected.src"
          :alt="t(selected.alt)"
          width="800"
          height="500"
          loading="lazy"
          decoding="async"
          class="block aspect-[8/5] w-full"
        />
      </Transition>
    </div>

    <figcaption class="mt-3 font-mono text-[10px] tracking-[0.15em] text-muted/70">
      {{ t(selected.alt) }}
    </figcaption>
  </figure>
</template>

<style scoped>
.scene-fade-enter-active,
.scene-fade-leave-active {
  transition: opacity 220ms var(--ease-out);
}
.scene-fade-enter-from,
.scene-fade-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .scene-fade-enter-active,
  .scene-fade-leave-active {
    transition: none;
  }
}
</style>
