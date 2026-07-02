<template>
  <div class="job-list-container">
    <h2 class="title">Available Jobs</h2>
    <ul class="job-list">
      <li v-for="job in jobs" :key="job.job_id" class="job-item">
        <router-link :to="{ name: 'JobDetail', params: { id: job.job_id } }" class="job-link">
          <div class="job-info">
            <span class="job-title">{{ job.job_title }}</span>
            <span class="job-id">{{ job.job_id }}</span>
          </div>
        </router-link>
      </li>
    </ul>
    <div v-if="jobs.length === 0" class="no-jobs">
      No jobs available at the moment.
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

