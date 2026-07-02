<template>
  <div id="app">
    <nav>
      <router-link to="/">Job List</router-link> | 
      <router-link to="/overview">Overview</router-link> | 
      <router-link to="/explorer">Explorer</router-link> | 
      <router-link to="/todo">Tasks</router-link>
      <!-- <router-link to="/application-form">Application Form</router-link> -->
      
    </nav>
    <router-view />
  </div>
</template>

<script setup>
</script>

<style>
@import "style.css";
@import "styles/App.css";
</style>
