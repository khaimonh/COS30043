<template>
  <div id="app" class="min-vh-100 px-3 py-4">
    <header class="mb-5">
      <nav>
        <router-link to="/" class="nav-link">Jobs</router-link> 
        <router-link to="/overview" class="nav-link">Overview</router-link> 
        <router-link to="/explorer" class="nav-link">Explorer</router-link> 
        <router-link to="/todo" class="nav-link">Tasks</router-link>
      </nav>
    </header>
    <main class="fade-in">
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>

<style>
@import "style.css";
</style>
