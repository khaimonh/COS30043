<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-12 col-lg-10">
        <div v-if="job" class="row g-4">
          <!-- Main Detail Cell -->
          <div class="col-12 col-md-8">
            <div class="bento-cell p-4 h-100">
              <h1 class="display-text mb-4">{{ job.job_title }}</h1>
              <p class="lead text-muted-bento mb-5">{{ job.job_description }}</p>
              
              <h3 class="h5 mb-4">Technical Requirements</h3>
              <div class="row g-3">
                <div v-for="skill in job.required_skills" :key="skill" class="col-6 col-sm-4">
                  <div class="p-2 rounded-3 border border-secondary text-center small bg-dark">
                    {{ skill }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Info Sidebar Cell -->
          <div class="col-12 col-md-4">
            <div class="bento-cell bento-cell-alt p-4 h-100">
              <h3 class="h6 text-dim mb-4">Role Metadata</h3>
              
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Organization</label>
                <span class="fw-bold">{{ job.company }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Location</label>
                <span class="fw-bold">{{ job.location }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Expected Salary</label>
                <span class="fw-bold">{{ job.salary_range }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Employment Type</label>
                <span class="fw-bold">{{ job.employment_type }}</span>
              </div>
              
              <router-link to="/application-form" class="btn btn-primary w-100 mt-4">Apply Now</router-link>
            </div>
          </div>
          
          <div class="col-12 text-center mt-4">
            <router-link to="/" class="text-muted-bento small">← Return to Registry</router-link>
          </div>
        </div>
        
        <div v-else class="text-center py-5">
          <div class="bento-cell p-5 mx-auto" style="max-width: 400px">
            <p class="display-text h4">Record Not Found</p>
            <router-link to="/" class="btn btn-primary">Back to Index</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import jobsData from '../data/jobs.json';

const route = useRoute();
const job = computed(() => {
  return jobsData.find(j => j.job_id === route.params.id);
});
</script>
