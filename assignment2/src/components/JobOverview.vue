<template>
  <div class="overview-container container">
    <div class="row">
      <div class="col-12">
        <h1 class="display-text">Dashboard Overview</h1>
      </div>
    </div>
    <div class="row">
      <div class="col-4">
        <div class="stat-card">
          <h3 class="display-text">Total Jobs</h3>
          <p class="stat-value">{{ jobsCount }}</p>
        </div>
      </div>
      <div class="col-4">
        <div class="stat-card">
          <h3 class="display-text">Categories</h3>
          <p class="stat-value">{{ categoriesCount }}</p>
        </div>
      </div>
      <div class="col-4">
        <div class="stat-card">
          <h3 class="display-text">Active Applications</h3>
          <p class="stat-value">0</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-12 col-md-8 offset-md-2">
        <section class="welcome-section">
          <h2 class="display-text">Welcome to the Job Portal</h2>
          <p>Browse through the latest opportunities in AI, Data Science, and Software Development. Find the role that matches your skills and apply today!</p>
        </section>
      </div>
    </div>
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
@import "../styles/JobOverview.css";
</style>
