<template>
  <div id="app" class="min-vh-100 px-3 py-4">
    <header class="main-header mb-5">
      <nav class="main-nav">
        <div class="nav-brand">
          <span class="brand-dot"></span>
          <span class="brand-text">JobPortal</span>
        </div>
        <div class="nav-links">
          <router-link to="/" class="nav-item">
            <span class="nav-label">Jobs</span>
            <div class="nav-indicator"></div>
          </router-link> 
          <router-link to="/overview" class="nav-item">
            <span class="nav-label">Overview</span>
            <div class="nav-indicator"></div>
          </router-link> 
          <router-link to="/explorer" class="nav-item">
            <span class="nav-label">Explorer</span>
            <div class="nav-indicator"></div>
          </router-link> 
          <router-link to="/todo" class="nav-item">
            <span class="nav-label">Tasks</span>
            <div class="nav-indicator"></div>
          </router-link>
        </div>
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
