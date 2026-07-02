<template>
  <div class="job-detail-container container">
    <div class="row">
      <div class="col-12 col-md-10 offset-md-1">
        <div v-if="job" class="job-card">
          <h1 class="display-text">{{ job.job_title }}</h1>
          <div class="row job-meta">
            <div class="col-4">
              <p><strong>ID:</strong> {{ job.job_id }}</p>
            </div>
            <div class="col-4">
              <p><strong>Company:</strong> {{ job.company }}</p>
            </div>
            <div class="col-4">
              <p><strong>Location:</strong> {{ job.location }}</p>
            </div>
          </div>
          
          <div class="row">
            <div class="col-12">
              <section>
                <h3 class="display-text">Description</h3>
                <p>{{ job.job_description }}</p>
              </section>
            </div>
          </div>

          <div class="row">
            <div class="col-12">
              <section>
                <h3 class="display-text">Requirements</h3>
                <ul>
                  <li v-for="skill in job.required_skills" :key="skill">{{ skill }}</li>
                </ul>
              </section>
            </div>
          </div>

          <div class="row">
            <div class="col-12">
              <section>
                <h3 class="display-text">Additional Details</h3>
                <div class="row">
                  <div class="col-4">
                    <p><strong>Salary:</strong> {{ job.salary_range }}</p>
                  </div>
                  <div class="col-4">
                    <p><strong>Type:</strong> {{ job.employment_type }}</p>
                  </div>
                  <div class="col-4">
                    <p><strong>Level:</strong> {{ job.job_level }}</p>
                  </div>
                </div>
              </section>
            </div>
          </div>

          <div class="row actions">
            <div class="col-6">
              <router-link to="/application-form" class="apply-btn">Apply Now</router-link>
            </div>
            <div class="col-6 text-right">
              <router-link to="/" class="back-btn">Back to List</router-link>
            </div>
          </div>
        </div>
        <div v-else class="error-msg">
          <p>Job not found.</p>
          <router-link to="/">Return to Job List</router-link>
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

<style scoped>
@import "../styles/JobDetail.css";
</style>
