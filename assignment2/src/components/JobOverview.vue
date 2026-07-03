<template>
  <div class="container py-5">
    <div class="row g-4">
      <!-- Main Hero: Asymmetric Anchor -->
      <div class="col-12 col-lg-8">
        <div class="bento-cell bento-cell-alt p-lg-5">
          <div class="flex-grow-1">
            <h1 class="display-text">Career Hub</h1>
            <p class="lead text-muted-bento mb-4" style="max-width: 600px; font-size: 1.2rem; line-height: 1.6;">
              Discover your next leap in technology. Explore a curated set of high-impact roles in AI and Software Engineering.
            </p>
            <router-link to="/" class="btn btn-primary w-auto">Browse Registry</router-link>
          </div>
          <div class="mt-5 pt-4 border-top border-secondary border-opacity-25">
            <div class="d-flex align-items-center gap-2">
              <span class="badge rounded-pill bg-dark border border-secondary text-muted px-3 py-2">V 2.0.4 Stable</span>
              <span class="text-dim small">Latest build: 2026-07-03</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Stats Stack: High-density metrics -->
      <div class="col-12 col-lg-4">
        <div class="row g-4 h-100">
          <div class="col-12">
            <div class="bento-cell text-center justify-content-center py-4">
              <h3 class="h6 text-dim mb-2">Openings</h3>
              <p class="stat-value mb-0">{{ jobsCount }}</p>
            </div>
          </div>
          <div class="col-12">
            <div class="bento-cell text-center justify-content-center py-4">
              <h3 class="h6 text-dim mb-2">Specialties</h3>
              <p class="stat-value mb-0">{{ categoriesCount }}</p>
            </div>
          </div>
          <div class="col-12">
            <div class="bento-cell text-center justify-content-center py-4">
              <h3 class="h6 text-dim mb-2">Status</h3>
              <p class="stat-value mb-0">Active</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- System Notification: Wide grounding element -->
      <div class="col-12">
        <div class="bento-cell p-4">
          <div class="row align-items-center">
            <div class="col-md-8">
              <h3 class="h5 mb-2">Neural Matching Active</h3>
              <p class="text-muted-bento mb-0" style="font-size: 0.95rem;">
                Our matching algorithm is now prioritizing candidates based on skill-set alignment and portfolio quality.
              </p>
            </div>
            <div class="col-md-4 text-end d-none d-md-block">
              <div class="text-dim small">Synchronized 2m ago</div>
            </div>
          </div>
        </div>
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
