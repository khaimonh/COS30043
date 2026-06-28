<script setup>
import { ref } from 'vue'

const newTask = ref('')

const tasks = ref([
  'Study Vue',
  'Finish Assignment'
])

function addTask() {
  if (newTask.value.trim()) {
    tasks.value.push(newTask.value)
    newTask.value = ''
  }
}
</script>

<template>

<h1>Tasks</h1>

<input
  v-model="newTask"
  placeholder="Enter a task"
/>

<button @click="addTask">
  Add
</button>

<ul>

<li
v-for="(task,index) in tasks"
:key="index"
>

{{ task }}

</li>

</ul>

</template>