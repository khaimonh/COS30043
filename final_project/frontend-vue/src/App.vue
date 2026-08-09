<script setup lang="ts">
import { RouterView } from "vue-router";
import ObiBand from "./components/layout/ObiBand.vue";
import Footer from "./components/layout/Footer.vue";
</script>

<template>
  <ObiBand />
  <main class="min-h-screen pb-5">
    <RouterView />
  </main>
  <Footer />
</template>
