<template>
  <div class="overview-container">
    <h1>Dashboard Overview</h1>
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Total Jobs</h3>
        <p class="stat-value">{{ jobsCount }}</p>
      </div>
      <div class="stat-card">
        <h3>Categories</h3>
        <p class="stat-value">{{ categoriesCount }}</p>
      </div>
      <div class="stat-card">
        <h3>Active Applications</h3>
        <p class="stat-value">0</p>
      </div>
    </div>
    
    <section class="welcome-section">
      <h2>Welcome to the Job Portal</h2>
      <p>Browse through the latest opportunities in AI, Data Science, and Software Development. Find the role that matches your skills and apply today!</p>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import jobsData from '../data/jobs.json';

const jobsCount = computed(() => jobsData.length);
const categoriesCount = computed(() => {
  const categories = new Set(jobsData.map(j => j.category));
  return categories.size;
});
</script>

