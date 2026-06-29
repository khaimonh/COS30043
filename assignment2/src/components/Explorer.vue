<template>
</template>

<script setup>
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
