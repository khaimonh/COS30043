<script setup>
import { ref, computed } from 'vue'

const firstName = ref('')
const lastName = ref('')
const selectedImage = ref('mountain')

const fullName = computed(() =>
  `${firstName.value} ${lastName.value}`.trim()
)
</script>

<template>

<h1>Home</h1>

<p>
  First Name:
  <input v-model="firstName">
</p>

<p>
  Last Name:
  <input v-model="lastName">
</p>

<h2 v-if="fullName">
  Welcome {{ fullName }}
</h2>

<h3>Select an image</h3>

<label>
  <input
    type="radio"
    value="mountain"
    v-model="selectedImage"
  >
  Mountain
</label>

<label style="margin-left:20px;">
  <input
    type="radio"
    value="ocean"
    v-model="selectedImage"
  >
  Ocean
</label>

<br><br>

<img
  :src="'/' + selectedImage + '.jpg'"
  width="500"
/>

</template>