<script setup>
import units from '../data/units.json'
</script>

<template>

<h1>Units</h1>

<table border="1" cellpadding="8">

<tr>
    <th>Code</th>
    <th>Unit Name</th>
    <th>Unit Credits</th>
    <th>Unit type</th>
</tr>

<tr
v-for="unit in units"
:key="unit.code"
>

<td>{{ unit.code }}</td>
<td>{{ unit.desc }}</td>
<td>{{ unit.cp }}</td>
<td>{{ unit.type }}</td>

</tr>

</table>

</template>