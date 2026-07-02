<template>
  <div class="job-list-container container">
    <div class="row">
      <div class="col-12 col-md-8 offset-md-2">
        <h2 class="title display-text">Available Jobs</h2>
        <ul class="job-list">
          <li v-for="job in jobs" :key="job.job_id" class="job-item">
            <router-link :to="{ name: 'JobDetail', params: { id: job.job_id } }" class="job-link">
              <div class="row job-info">
                <div class="col-8">
                  <span class="job-title">{{ job.job_title }}</span>
                </div>
                <div class="col-4 text-right">
                  <span class="job-id">{{ job.job_id }}</span>
                </div>
              </div>
            </router-link>
          </li>
        </ul>
        <div v-if="jobs.length === 0" class="no-jobs text-center">
          No jobs available at the moment.
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
  console.log('Loading jobs data:', jobsData);
  jobs.value = jobsData;
});
</script>

<style scoped>
@import "../styles/JobList.css";
</style>
