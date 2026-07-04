<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-lg-7">
        <div class="bento-cell p-4 p-lg-5">
          <div class="d-flex justify-content-between align-items-center mb-5">
            <h2 class="display-text mb-0">Application Pipeline</h2>
            <div class="text-dim small">
              {{ tasks.filter(t => !t.done).length }} Pending Tasks
            </div>
          </div>
          
          <div class="input-group mb-5 shadow-sm">
            <input 
              v-model="newItem" 
              @keyup.enter="addItem" 
              type="text" 
              class="form-control form-control-lg" 
              placeholder="Enter next milestone..." 
            />
            <button @click="addItem" class="btn btn-primary px-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                <path d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2z"/>
              </svg>
            </button>
          </div>
          
          <ul class="todo-list p-0 list-unstyled">
            <li v-for="(task, index) in tasks" :key="index" class="todo-item d-flex align-items-center p-3 mb-3">
              <div class="form-check">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  v-model="task.done" 
                  :id="'task-' + index"
                />
              </div>
              <div class="flex-grow-1 ms-3 d-flex align-items-center justify-content-between">
                <span :class="{ completed: task.done }" class="fw-medium text-main">
                  {{ task.text }}
                </span>
                
                <div class="d-flex align-items-center gap-2">
                  <div class="priority-badge" :class="task.priority.toLowerCase()">
                    {{ task.priority }}
                  </div>
                  <select 
                    v-model="task.priority" 
                    class="form-select form-select-sm py-0 px-2 text-main" 
                    style="width: auto; font-size: 0.7rem; background: transparent; border-color: var(--border-subtle);"
                  >
                    <option value="Low">Low</option>
                    <option value="High">High</option>
                  </select>
                </div>
              </div>
              <button @click="removeTask(index)" class="btn btn-link text-danger p-0 ms-3 text-decoration-none fw-bold" title="Delete Task">×</button>
            </li>
          </ul>

          <div v-if="tasks.length === 0" class="text-center py-5">
            <div class="text-dim mb-3">Pipeline is currently empty</div>
            <p class="small text-dim">Add a new milestone to get started.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const newItem = ref('');
const tasks = ref([
  { text: 'Optimize Portfolio', done: false, priority: 'High' },
  { text: 'Refine Resume', done: false, priority: 'Low' },
  { text: 'Mock Interview Prep', done: false, priority: 'High' },
]);

const addItem = () => {
  if (newItem.value.trim()) {
    tasks.value.push({ 
      text: newItem.value, 
      done: false, 
      priority: 'Low' 
    });
    newItem.value = '';
  }
};

const removeTask = (index) => {
  tasks.value.splice(index, 1);
};
</script>

<style scoped>
.todo-item {
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  transition: all 0.3s cubic-bezier(0.2, 0, 0, 1);
}

.todo-item:hover {
  border-color: var(--brand-primary);
  background: rgba(255, 255, 255, 0.06);
  transform: translateX(4px);
}

.completed span {
  text-decoration: line-through;
  color: var(--text-dim);
  opacity: 0.5;
}

.priority-badge {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.05em;
  transition: all 0.2s ease;
}

.priority-badge.high {
  background: oklch(0.6 0.15 20); /* Soft Red */
  color: oklch(0.9 0.05 20);
  border: 1px solid oklch(0.5 0.15 20);
}

.priority-badge.low {
  background: oklch(0.3 0.05 250); /* Deep Slate */
  color: var(--text-muted);
  border: 1px solid var(--border-subtle);
}

/* Custom scrollbar for long lists */
.todo-list {
  max-height: 60vh;
  overflow-y: auto;
  padding-right: var(--space-sm);
}

.todo-list::-webkit-scrollbar {
  width: 6px;
}
.todo-list::-webkit-scrollbar-track {
  background: transparent;
}
.todo-list::-webkit-scrollbar-thumb {
  background: var(--border-subtle);
  border-radius: 10px;
}
.todo-list::-webkit-scrollbar-thumb:hover {
  background: var(--text-dim);
}
</style>
