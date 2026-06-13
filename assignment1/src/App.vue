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

<style scoped>
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #3b82f6;
    color: white;
    padding: 8px 16px;
    text-decoration: none;
    border-radius: 4px;
    z-index: 100;
}

.skip-link:focus {
    top: 0;
}
</style>
