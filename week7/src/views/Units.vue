<script setup>
import units from '../data/units.json'
</script>

<template>

<h1>Units</h1>

<table border="1" cellpadding="8">
  <thead>
    <tr>
      <th>Code</th>
      <th>Unit Name</th>
      <th>Unit Credits</th>
      <th>Unit Type</th>
    </tr>
  </thead>

  <tbody>
    <tr
      v-for="unit in units"
      :key="unit.code"
    >
      <td>{{ unit.code }}</td>
      <td>{{ unit.desc }}</td>
      <td>{{ unit.cp }}</td>
      <td>{{ unit.type }}</td>
    </tr>
  </tbody>
</table>

</template>