<template>
  <div id="app">
    <nav>
      <router-link to="/">Job List</router-link> | 
      <router-link to="/overview">Overview</router-link> | 
      <router-link to="/explorer">Explorer</router-link> | 
      <router-link to="/todo">Tasks</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
// The router-view will render the component based on the current route
</script>

<style>
nav {
  padding: 1rem;
  background: #f4f4f4;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
  gap: 15px;
}
nav a {
  text-decoration: none;
  color: #2c3e50;
  font-weight: bold;
}
nav a:hover {
  color: #42b883;
}
</style>
