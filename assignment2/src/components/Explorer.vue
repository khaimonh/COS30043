<template>
  <div class="explorer-container">
    <h2>File & Resource Explorer</h2>
    <div class="explorer-layout">
      <div class="sidebar">
        <div v-for="folder in folders" :key="folder.name" class="folder">
          <span class="folder-header" @click="toggleFolder(folder.name)">
            📁 {{ folder.name }}
          </span>
          <div v-if="activeFolder === folder.name" class="files">
            <div v-for="file in folder.files" :key="file" class="file">
              📄 {{ file }}
            </div>
          </div>
        </div>
      </div>
      <div class="preview">
        <div v-if="selectedFile" class="file-content">
          <h3>Viewing: {{ selectedFile }}</h3>
          <p>Content for {{ selectedFile }} would be loaded here.</p>
        </div>
        <div v-else class="placeholder">
          Select a file to preview its content.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const activeFolder = ref(null);
const selectedFile = ref(null);

const folders = [
  { name: 'src', files: ['App.vue', 'main.js', 'router.js'] },
  { name: 'components', files: ['JobList.vue', 'JobDetail.vue', 'Overview.vue'] },
  { name: 'data', files: ['jobs.json'] },
  { name: 'assets', files: ['logo.png', 'style.css'] },
];

const toggleFolder = (name) => {
  activeFolder.value = activeFolder.value === name ? null : name;
};
</script>

<style scoped>
.explorer-container {
  max-width: 1000px;
  margin: 0 auto;
  font-family: sans-serif;
}
.explorer-layout {
  display: flex;
  height: 400px;
  border: 1px solid #ccc;
}
.sidebar {
  width: 250px;
  border-right: 1px solid #ccc;
  background: #f5f5f5;
  overflow-y: auto;
  padding: 10px;
}
.folder-header {
  cursor: pointer;
  display: block;
  padding: 5px;
  font-weight: bold;
}
.folder-header:hover {
  background: #ddd;
}
.files {
  padding-left: 20px;
}
.file {
  padding: 3px 0;
  cursor: pointer;
  font-size: 0.9rem;
}
.preview {
  flex: 1;
  padding: 20px;
  background: #fff;
}
.placeholder {
  color: #888;
  text-align: center;
  margin-top: 50px;
}
</style>
