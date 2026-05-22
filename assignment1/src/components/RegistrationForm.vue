<script setup>
import { computed, ref, watch } from 'vue'
import '../assets/styles/registrationForm.css'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')

const categories = ['Technology', 'Business', 'Marketing', 'Finance']

const eventsByCategory = {
    Technology: [
        'AI Innovation Summit',
        'Cloud Architecture Workshop',
        'Cybersecurity Essentials',
    ],
    Business: [
        'Business Growth Conference',
        'Leadership Excellence Forum',
        'Startup Strategy Bootcamp',
    ],
    Marketing: [
        'Digital Marketing Masterclass',
        'Brand Storytelling Workshop',
        'Social Media Growth Lab',
    ],
    Finance: [
        'Personal Finance Planning',
        'Investment Fundamentals Seminar',
        'Corporate Finance Essentials',
    ],
}

const selectedCategory = ref('Business')
const eventOptions = computed(
    () => eventsByCategory[selectedCategory.value] || []
)
const selectedEventName = ref(eventOptions.value[0] || '')

watch(selectedCategory, () => {
    selectedEventName.value = eventOptions.value[0] || ''
})

const showPasswordMismatch = computed(() => {
    if (confirmPassword.value.length === 0) return false

    return password.value !== confirmPassword.value
})

const canShowSummary = computed(() => {
    return (
        username.value.trim().length > 0 && selectedEventName.value.length > 0
    )
})
</script>

<template>
    <section id="registration-form">
        <div class="container py-5">
            <div class="row mb-4">
                <div class="col-12">
                    <h1 class="page-title">Registration Form</h1>
                </div>
            </div>

            <div class="row g-4">
                <div class="col-12">
                    <div class="form-card">
                        <h2 class="section-title">User Details</h2>

                        <div class="row g-3 form-layout">
                            <div class="col-12 col-md-6">
                                <div class="form-group">
                                    <label for="username" class="form-label"
                                        >Username</label
                                    >
                                    <input
                                        id="username"
                                        v-model="username"
                                        type="text"
                                        class="form-control"
                                        placeholder="Enter username"
                                    />
                                </div>
                            </div>

                            <div class="col-12 col-md-6">
                                <div class="form-group">
                                    <label for="password" class="form-label"
                                        >Password</label
                                    >
                                    <input
                                        id="password"
                                        v-model="password"
                                        type="password"
                                        class="form-control"
                                        placeholder="Enter password"
                                    />
                                </div>
                            </div>

                            <div class="col-12">
                                <div class="form-group confirm-password-row">
                                    <label
                                        for="confirm-password"
                                        class="form-label"
                                        >Confirm Password</label
                                    >
                                    <div class="confirm-password-content">
                                        <input
                                            id="confirm-password"
                                            v-model="confirmPassword"
                                            type="password"
                                            class="form-control"
                                            placeholder="Confirm password"
                                        />
                                        <span
                                            v-if="showPasswordMismatch"
                                            class="mismatch-message"
                                        >
                                            Passwords do not match.
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div class="col-12">
                                <div class="form-group">
                                    <p class="form-label mb-2">
                                        Event Category
                                    </p>
                                    <div class="category-options">
                                        <label
                                            v-for="category in categories"
                                            :key="category"
                                            class="category-option form-check form-check-inline"
                                        >
                                            <input
                                                v-model="selectedCategory"
                                                type="radio"
                                                name="event-category"
                                                class="form-check-input"
                                                :value="category"
                                            />
                                            <span class="form-check-label">{{
                                                category
                                            }}</span>
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <div class="col-12">
                                <div class="form-group">
                                    <label for="event-name" class="form-label"
                                        >Event Name</label
                                    >
                                    <select
                                        id="event-name"
                                        v-model="selectedEventName"
                                        class="form-select"
                                    >
                                        <option
                                            v-for="eventName in eventOptions"
                                            :key="eventName"
                                            :value="eventName"
                                        >
                                            {{ eventName }}
                                        </option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-12" v-if="canShowSummary">
                    <div class="summary-section">
                        <h2 class="section-title">Registration Summary</h2>
                        <p><strong>Username:</strong> {{ username }}</p>
                        <p>
                            <strong>Selected category:</strong>
                            {{ selectedCategory }}
                        </p>
                        <p>
                            <strong>Selected event name:</strong>
                            {{ selectedEventName }}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
