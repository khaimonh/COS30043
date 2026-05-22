<script setup>
import { ref, onMounted } from 'vue'
import '../assets/styles/eventInformation.css'

const events = ref([])

onMounted(async () => {
    try {
        const response = await fetch('/events.txt')
        const text = await response.text()
        events.value = eval(text)
    } catch (error) {
        console.error('Error loading events:', error)
    }
})
</script>

<template>
    <section id="event-information">
        <div class="container py-5">
            <div class="row mb-4">
                <div class="col-12">
                    <h1 class="page-title">Event Information</h1>
                </div>
            </div>

            <div class="row g-4 mb-4">
                <div class="col-12">
                    <div class="filter-section">
                        <h2 class="section-title">Filter Events</h2>

                        <div class="row g-3 filter-inputs">
                            <div class="col-12 col-md-4">
                                <div class="input-group-custom">
                                    <label for="event-id-search"
                                        >Search by Event ID</label
                                    >
                                    <input
                                        class="form-control"
                                        type="text"
                                        id="event-id-search"
                                        placeholder="Enter Event ID"
                                    />
                                </div>
                            </div>

                            <div class="col-12 col-md-4">
                                <div class="input-group-custom">
                                    <label for="event-name-search"
                                        >Search by Event Name</label
                                    >
                                    <input
                                        class="form-control"
                                        type="text"
                                        id="event-name-search"
                                        placeholder="Enter Event Name"
                                    />
                                </div>
                            </div>

                            <div class="col-12 col-md-4">
                                <div class="input-group-custom">
                                    <label for="duration-search"
                                        >Search by Duration (hours)</label
                                    >
                                    <input
                                        class="form-control"
                                        type="text"
                                        id="duration-search"
                                        placeholder="Enter Duration"
                                    />
                                </div>
                            </div>
                        </div>

                        <div class="filter-category mt-4">
                            <p class="category-label mb-2">
                                Filter by Category
                            </p>
                            <div class="radio-group">
                                <div
                                    class="form-check form-check-inline radio-item"
                                >
                                    <input
                                        class="form-check-input"
                                        type="radio"
                                        id="category-all"
                                        name="category"
                                        value="All"
                                        checked
                                    />
                                    <label
                                        class="form-check-label"
                                        for="category-all"
                                        >All</label
                                    >
                                </div>
                                <div
                                    class="form-check form-check-inline radio-item"
                                >
                                    <input
                                        class="form-check-input"
                                        type="radio"
                                        id="category-technology"
                                        name="category"
                                        value="Technology"
                                    />
                                    <label
                                        class="form-check-label"
                                        for="category-technology"
                                        >Technology</label
                                    >
                                </div>
                                <div
                                    class="form-check form-check-inline radio-item"
                                >
                                    <input
                                        class="form-check-input"
                                        type="radio"
                                        id="category-business"
                                        name="category"
                                        value="Business"
                                    />
                                    <label
                                        class="form-check-label"
                                        for="category-business"
                                        >Business</label
                                    >
                                </div>
                                <div
                                    class="form-check form-check-inline radio-item"
                                >
                                    <input
                                        class="form-check-input"
                                        type="radio"
                                        id="category-marketing"
                                        name="category"
                                        value="Marketing"
                                    />
                                    <label
                                        class="form-check-label"
                                        for="category-marketing"
                                        >Marketing</label
                                    >
                                </div>
                                <div
                                    class="form-check form-check-inline radio-item"
                                >
                                    <input
                                        class="form-check-input"
                                        type="radio"
                                        id="category-finance"
                                        name="category"
                                        value="Finance"
                                    />
                                    <label
                                        class="form-check-label"
                                        for="category-finance"
                                        >Finance</label
                                    >
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-12">
                    <div class="events-table-section">
                        <h2 class="section-title">Events</h2>
                        <div class="table-responsive">
                            <table
                                id="events-table"
                                class="table table-striped table-hover align-middle mb-0"
                            >
                                <thead>
                                    <tr>
                                        <th>Event ID</th>
                                        <th>Event Name</th>
                                        <th>Category</th>
                                        <th>Duration Hours</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="event in events" :key="event.eventid">
                                        <td>{{ event.eventid }}</td>
                                        <td>{{ event.eventname }}</td>
                                        <td>{{ event.category }}</td>
                                        <td>{{ event.durationhour }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
