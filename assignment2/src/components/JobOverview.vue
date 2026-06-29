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

<style scoped>
.overview-container {
  max-width: 1000px;
  margin: 0 auto;
  font-family: sans-serif;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 2rem 0;
}
.stat-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 10px;
  text-align: center;
  border: 1px solid #ddd;
}
.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #42b883;
  margin: 0;
}
.welcome-section {
  background: #eefaf5;
  padding: 2rem;
  border-radius: 12px;
  margin-top: 2rem;
}
</style>
