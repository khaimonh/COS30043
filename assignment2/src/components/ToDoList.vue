<template>
  <div class="todo-container container">
    <div class="row">
      <div class="col-12 col-md-6 offset-md-3">
        <h2 class="display-text">Application Checklist</h2>
        <div class="input-group">
          <input v-model="newItem" @keyup.enter="addItem" placeholder="Add a new task..." />
          <button @click="addItem">Add</button>
        </div>
        <ul class="todo-list">
          <li v-for="(task, index) in tasks" :key="index" :class="{ completed: task.done }">
            <div class="task-item">
              <input type="checkbox" v-model="task.done" />
              <span v-if="task.text">{{ task.text }}</span>
              <button @click="removeTask(index)" class="delete-btn">×</button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const newItem = ref('');
const tasks = ref([
  { text: 'Update Resume', done: false },
  { text: 'Write Cover Letter', done: false },
  { text: 'Prepare Portfolio', done: false },
]);

const addItem = () => {
  if (newItem.value.trim()) {
    tasks.value.push({ text: newItem.value, done: false });
    newItem.value = '';
  }
};

const removeTask = (index) => {
  tasks.value.splice(index, 1);
};
</script>

<style scoped>
@import "../styles/ToDoList.css";
</style>
