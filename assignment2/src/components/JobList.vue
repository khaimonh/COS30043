<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-lg-10">
        <div class="row align-items-end mb-5">
          <div class="col-12 col-lg-8">
            <h1 class="display-text">Opportunities</h1>
            <p class="text-muted-bento lead mb-0" style="max-width: 500px; font-size: 1.1rem; line-height: 1.5;">
              A curated registry of high-impact engineering roles. Filtered for quality, technical depth, and growth potential.
            </p>
          </div>
          <div class="col-12 col-lg-4 text-lg-end mt-4 mt-lg-0">
            <div class="d-inline-flex align-items-center gap-3">
              <span class="text-dim small">{{ jobs.length }} Roles Available</span>
              <div class="dropdown">
                <button class="btn btn-outline-secondary btn-sm rounded-pill px-3 text-main" type="button" data-bs-toggle="dropdown">
                  Sort by: Newest
                </button>
                <ul class="dropdown-menu dropdown-menu-end bg-surface border-subtle">
                  <li><a class="dropdown-item text-main" href="#">Newest First</a></li>
                  <li><a class="dropdown-item text-main" href="#">Highest Salary</a></li>
                  <li><a class="dropdown-item text-main" href="#">A-Z Company</a></li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        
        <div class="row g-4">
          <div v-for="job in jobs" :key="job.job_id" class="col-12 col-xl-6">
            <div class="bento-cell job-card group">
              <router-link :to="{ name: 'JobDetail', params: { id: job.job_id } }" class="text-decoration-none w-100 h-100 d-flex flex-column">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <div class="d-flex align-items-center gap-3">
                    <div class="company-icon">
                      {{ job.company.charAt(0) }}
                    </div>
                    <div>
                      <h3 class="h5 text-main mb-0">{{ job.job_title }}</h3>
                      <span class="text-dim small">{{ job.company }}</span>
                    </div>
                  </div>
                  <span class="badge rounded-pill bg-dark border border-secondary text-muted px-2 py-1 small">
                    #{{ job.job_id }}
                  </span>
                </div>
                
                <div class="row g-3 mb-4">
                  <div class="col-6">
                    <div class="text-dim small">Location</div>
                    <div class="text-main fw-medium">{{ job.location }}</div>
                  </div>
                  <div class="col-6">
                    <div class="text-dim small">Salary Range</div>
                    <div class="text-main fw-medium">{{ job.salary_range }}</div>
                  </div>
                </div>

                <div class="mt-auto d-flex justify-content-between align-items-center">
                  <div class="d-flex gap-2">
                    <span v-for="skill in job.required_skills.slice(0, 2)" :key="skill" class="badge bg-dark border border-secondary text-dim small">
                      {{ skill }}
                    </span>
                    <span v-if="job.required_skills.length > 2" class="badge bg-dark border border-secondary text-dim small">
                      +{{ job.required_skills.length - 2 }} more
                    </span>
                  </div>
                  <div class="btn-arrow">
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </div>
        
        <div v-if="jobs.length === 0" class="bento-cell text-center py-5 mt-4">
          <p class="text-muted-bento">No openings found in the database.</p>
          <router-link to="/overview" class="btn btn-primary w-auto mt-3">Return to Hub</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import jobsData from '../data/jobs.json';

const jobs = ref([]);

onMounted(() => {
  jobs.value = jobsData;
});
</script>

<style scoped>
.job-card {
  cursor: pointer;
  border-color: var(--border-subtle);
}

.job-card:hover {
  border-color: var(--brand-primary);
}

.company-icon {
  width: 40px;
  height: 40px;
  background: var(--bg-surface-alt);
  border: 1px solid var(--border-strong);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: var(--brand-primary);
  flex-shrink: 0;
}

.btn-arrow {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-main);
  border: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-dim);
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.job-card:hover .btn-arrow {
  background: var(--brand-primary);
  color: var(--bg-main);
  border-color: var(--brand-primary);
  transform: translateX(3px);
}
</style>
