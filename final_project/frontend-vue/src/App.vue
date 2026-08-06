<script setup lang="ts">
import { RouterView } from "vue-router";
import Navbar from "./components/layout/Navbar.vue";
import Footer from "./components/layout/Footer.vue";
</script>

<template>
  <Navbar />
  <main class="pt-20 sm:pt-24">
    <RouterView />
  </main>
  <Footer />
</template>
