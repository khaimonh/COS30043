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

<style scoped>
.job-list-container {
  max-width: 800px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
  padding: 20px;
}
.title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}
.job-list {
  list-style: none;
  padding: 0;
}
.job-item {
  margin-bottom: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: transform 0.1s, box-shadow 0.1s;
}
.job-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.job-link {
  text-decoration: none;
  color: inherit;
  display: block;
  padding: 15px;
}
.job-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.job-title {
  font-weight: bold;
  font-size: 1.1rem;
  color: #333;
}
.job-id {
  color: #888;
  font-size: 0.9rem;
  font-family: monospace;
}
.no-jobs {
  text-align: center;
  color: #666;
  margin-top: 2rem;
}
</style>
