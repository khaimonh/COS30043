<template>
  <div>

    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/tasks">Tasks</router-link> |
      <router-link to="/units">Units</router-link>
    </nav>

    <hr>

    <router-view />

  </div>
</template>

<style>
body{
  font-family: Arial;
}

nav{
  margin-bottom:20px;
}

nav a{
  margin-right:20px;
}
</style>