<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-lg-7">
        <div class="bento-cell p-4 p-lg-5">
          <div class="d-flex justify-content-between align-items-center mb-5">
            <h2 class="display-text mb-0">Application Pipeline</h2>
            <div class="text-dim small">
              {{ pendingCount }} Pending Tasks
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
            <li v-for="(task, index) in sortedTasks" :key="task.id" class="todo-item d-flex align-items-center p-3 mb-3">
              <div class="form-check">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  v-model="task.done" 
                  :id="'task-' + task.id"
                />
              </div>
              <div class="flex-grow-1 ms-3 d-flex align-items-center justify-content-between">
                <span :class="{ completed: task.done }" class="fw-medium text-main">
                  {{ task.text }}
                </span>
                
                <div class="d-flex align-items-center gap-2">
                  <button 
                    @click="togglePriority(task)" 
                    class="priority-toggle-btn" 
                    :class="task.priority.toLowerCase()"
                  >
                    <span class="priority-label">{{ task.priority }}</span>
                  </button>
                </div>
              </div>
              <button @click="removeTask(task.id)" class="btn btn-link text-danger p-0 ms-3 text-decoration-none fw-bold" title="Delete Task">×</button>
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
import { ref, computed } from 'vue';

const newItem = ref('');
const tasks = ref([
  { id: 1, text: 'Optimize Portfolio', done: false, priority: 'High' },
  { id: 2, text: 'Refine Resume', done: false, priority: 'Low' },
  { id: 3, text: 'Mock Interview Prep', done: false, priority: 'High' },
]);

const pendingCount = computed(() => tasks.value.filter(t => !t.done).length);

const sortedTasks = computed(() => {
  return [...tasks.value].sort((a, b) => {
    if (a.done !== b.done) return a.done ? 1 : -1;
    
    if (a.priority !== b.priority) {
      return a.priority === 'High' ? -1 : 1;
    }
    
    return 0;
  });
});

const addItem = () => {
  if (newItem.value.trim()) {
    tasks.value.push({ 
      id: Date.now(),
      text: newItem.value, 
      done: false, 
      priority: 'Low' 
    });
    newItem.value = '';
  }
};

const removeTask = (id) => {
  tasks.value = tasks.value.filter(t => t.id !== id);
};

const togglePriority = (task) => {
  task.priority = task.priority === 'High' ? 'Low' : 'High';
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

.priority-toggle-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 4px 8px;
  border-radius: 6px;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  outline: none;
}

.priority-toggle-btn.high {
  background: oklch(0.6 0.15 20); 
  color: oklch(0.9 0.05 20);
  border-color: oklch(0.5 0.15 20);
}

.priority-toggle-btn.low {
  background: oklch(0.3 0.05 250); 
  color: var(--text-muted);
  border-color: var(--border-subtle);
}

.priority-toggle-btn:hover {
  filter: brightness(1.2);
  transform: scale(1.05);
}

.priority-label {
  line-height: 1;
}

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
