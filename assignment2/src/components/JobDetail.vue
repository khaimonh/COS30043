<template>
  <div class="job-detail-container">
    <div v-if="job" class="job-card">
      <h1>{{ job.job_title }}</h1>
      <div class="job-meta">
        <p><strong>ID:</strong> {{ job.job_id }}</p>
        <p><strong>Company:</strong> {{ job.company }}</p>
        <p><strong>Location:</strong> {{ job.location }}</p>
      </div>
      
      <section>
        <h3>Description</h3>
        <p>{{ job.job_description }}</p>
      </section>

      <section>
        <h3>Requirements</h3>
        <ul>
          <li v-for="skill in job.required_skills" :key="skill">{{ skill }}</li>
        </ul>
      </section>

      <section>
        <h3>Additional Details</h3>
        <p><strong>Salary:</strong> {{ job.salary_range }}</p>
        <p><strong>Type:</strong> {{ job.employment_type }}</p>
        <p><strong>Level:</strong> {{ job.job_level }}</p>
      </section>

      <div class="actions">
        <router-link to="/application-form" class="apply-btn">Apply Now</router-link>
        <router-link to="/" class="back-btn">Back to List</router-link>
      </div>
    </div>
    <div v-else class="error-msg">
      <p>Job not found.</p>
      <router-link to="/">Return to Job List</router-link>
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

<style scoped>
.job-detail-container {
  max-width: 800px;
  margin: 2rem auto;
  font-family: sans-serif;
}
.job-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.job-meta {
  display: flex;
  gap: 20px;
  color: #666;
  margin-bottom: 1.5rem;
}
section {
  margin-bottom: 1.5rem;
  border-top: 1px solid #eee;
  padding-top: 1rem;
}
.actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}
.apply-btn {
  background: #42b883;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
}
.back-btn {
  color: #666;
  text-decoration: none;
  align-self: center;
}
.error-msg {
  text-align: center;
  margin-top: 3rem;
}
</style>
