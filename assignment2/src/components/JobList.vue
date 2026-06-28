<template>
  <div>
    <h2>Job List</h2>
    <ul>
      <li>
        <router-link to="/">Overview</router-link>
      </li>
      <li v-for="job in jobs" :key="job.id">
        <router-link :to="{ name: 'JobDetail', params: { id: job.id } }">
          Job {{ job.id }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import jobsData from '../../jobs.txt'; //import jobs data

export default {
  data() {
    return {
      jobs: jobsData,
    };
  },
};
</script>
