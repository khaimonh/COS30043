<template>
  <div class="container-fluid py-5">
    <div class="row g-4">
      <div class="col-12 col-md-3 col-lg-3">
        <div class="bento-cell p-3 h-100">
          <h3 class="h6 text-muted-bento mb-4 uppercase-tracked">Registry Explorer</h3>
          
          <div class="nav flex-column gap-2">
            <router-link 
              to="/" 
              class="nav-link p-3 rounded-3 text-main d-flex align-items-center gap-2"
              active-class="active-explorer-link"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-grid" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M1 3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V3zm1 1v10a.5.5 0 0 0 .5.5h12a.5.5 0 0 0 .5-.5V4a.5.5 0 0 0-.5-.5H2a.5.5 0 0 0-.5.5z"/>
                <path d="M2 6a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-1 0v-1H2.5A.5.5 0 0 1 2 6zm0 3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-1 0v-1H2.5A.5.5 0 0 1 2 9zm0 3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-1 0v-1H2.5A.5.5 0 0 1 2 12z"/>
              </svg>
              Overview
            </router-link>
            
            <hr class="my-3 border-secondary opacity-25" />
            
            <div class="d-flex flex-column gap-2">
              <router-link 
                v-for="job in jobs" 
                :key="job.job_id" 
                :to="{ name: 'ExplorerJobDetail', params: { id: job.job_id } }" 
                class="nav-link p-3 rounded-3 text-main d-flex align-items-center justify-content-between"
                active-class="active-explorer-link"
              >
                <span class="small">ID: {{ job.job_id }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-chevron-right" viewBox="0 0 16 16">
                  <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10 9.293H1.5a.5.5 0 0 1 0-1h8.5l-6-6a.5.5 0 0 1 0-.708z"/>
                </svg>
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-12 col-md-9 col-lg-9">
        <div class="bento-cell h-100">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import jobsData from '../data/jobs.json';
const jobs = jobsData;
</script>

<style scoped>
.active-explorer-link {
  background: var(--brand-primary) !important;
  color: var(--bg-main) !important;
  font-weight: 600;
}

.nav-link {
  transition: all 0.2s ease;
  cursor: pointer;
}

.nav-link:hover:not(.active-explorer-link) {
  background: var(--bg-surface-alt);
  color: var(--text-main) !important;
}
</style>
