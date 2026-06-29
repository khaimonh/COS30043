<template>
  <div class="todo-container">
    <h2>Application Checklist</h2>
    <div class="input-group">
      <input v-model="newItem" @keyup.enter="addItem" placeholder="Add a new task..." />
      <button @click="addItem">Add</button>
    </div>
    <ul class="todo-list">
      <li v-for="(task, index) in tasks" :key="index" :class="{ completed: task.done }">
        <div class="task-item">
          <input type="checkbox" v-model="task.done" />
          <span>{{ task.text }}</span>
          <button @click="removeTask(index)" class="delete-btn">×</button>
        </div>
      </li>
    </ul>
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
.todo-container {
  max-width: 500px;
  margin: 0 auto;
  font-family: sans-serif;
}
.input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
input[type="text"] {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 8px 15px;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.todo-list {
  list-style: none;
  padding: 0;
}
.task-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
  gap: 10px;
}
.completed span {
  text-decoration: line-through;
  color: #888;
}
.delete-btn {
  margin-left: auto;
  background: #ff5f5f;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  padding: 0;
  line-height: 1;
  font-weight: bold;
}
</style>
