<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-12 col-lg-10">
        <div v-if="job" class="row g-4">
          <div class="col-12 col-md-8">
            <div class="bento-cell p-4 h-100">
              <div class="d-flex justify-content-between align-items-start mb-4">
                <h1 class="display-text mb-0">{{ job.job_title }}</h1>
                <span class="badge rounded-pill bg-dark border border-secondary text-muted-bento px-3 py-2">#{{ job.job_id }}</span>
              </div>
              
              <p class="lead text-muted-bento mb-5" style="line-height: 1.6;">{{ job.job_description }}</p>
              
              <div class="row g-4">
                <div class="col-12">
                  <h3 class="h5 mb-3">Technical Requirements</h3>
                  <div class="row g-2">
                    <div v-for="skill in job.required_skills" :key="skill" class="col-6 col-sm-4">
                      <div class="p-2 rounded-3 border border-secondary text-center small bg-dark">
                        {{ skill }}
                      </div>
                    </div>
                  </div>
                </div>

                <div class="col-12">
                  <h3 class="h5 mb-3">Preferred Qualifications</h3>
                  <div class="row g-2">
                    <div v-for="pref in job.preferred_qualifications" :key="pref" class="col-6 col-sm-4">
                      <div class="p-2 rounded-3 border border-secondary text-center small bg-dark bg-opacity-50">
                        {{ pref }}
                      </div>
                    </div>
                  </div>
                </div>

                <div class="col-12">
                  <div class="d-flex flex-wrap gap-2 mt-3">
                    <span v-for="tag in job.tags" :key="tag" class="badge rounded-pill bg-surface border border-secondary text-dim small">
                      #{{ tag }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Info Sidebar Cell -->
          <div class="col-12 col-md-4">
            <div class="bento-cell bento-cell-alt p-4 h-100">
              <h3 class="h6 text-dim mb-4 uppercase-tracked">Role Metadata</h3>
              
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Organization</label>
                <span class="fw-bold text-main">{{ job.company }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Supervisor</label>
                <span class="fw-bold text-main">{{ job.supervisor }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Location</label>
                <span class="fw-bold text-main">{{ job.location }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Expected Salary</label>
                <span class="fw-bold text-main">{{ job.salary_range }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Employment Type</label>
                <span class="fw-bold text-main">{{ job.employment_type }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Job Level</label>
                <span class="fw-bold text-main">{{ job.job_level }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Positions Available</label>
                <span class="fw-bold text-main">{{ job.positions_available }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Posted Date</label>
                <span class="fw-bold text-main">{{ job.posted_date }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Application Deadline</label>
                <span class="fw-bold text-main">{{ job.application_deadline }}</span>
              </div>
              <div class="mb-4">
                <label class="small text-dim d-block mb-1">Start Date</label>
                <span class="fw-bold text-main">{{ job.start_date }}</span>
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
