<script setup>
// import HelloWorld from './components/HelloWorld.vue'
import Introduction from './components/Introduction.vue'
import EventInformation from './components/EventInformation.vue'
import RegistrationForm from './components/RegistrationForm.vue'
</script>

<template>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <!-- <HelloWorld /> -->
    <Introduction />
    <div id="main-content">
        <EventInformation />
        <RegistrationForm />
    </div>
</template>
