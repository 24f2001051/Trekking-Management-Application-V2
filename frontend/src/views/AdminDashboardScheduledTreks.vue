<template>
    <DashNavbar />

    <div class="d-flex">
        <AdminSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Scheduled Treks</h2>

                <button class="btn btn-outline-primary" @click="getschedules" :disabled="loading"> Refresh </button>
            </div>

            <p class="text-muted mb-4">View all upcoming and ongoing trekking schedules.</p>

            <div class="row g-3 mb-4">

                <div class="col-md-4">
                    <div class="card shadow-sm h-100">
                        <div class="card-body">
                            <p class="text-muted mb-1">Upcoming Schedules</p>
                            <h3 class="mb-0">{{ upcomingCount }}</h3>
                        </div>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card shadow-sm h-100">
                        <div class="card-body">
                            <p class="text-muted mb-1">Ongoing Schedules</p>
                            <h3 class="mb-0">{{ ongoingCount }}</h3>
                        </div>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card shadow-sm h-100">
                        <div class="card-body">
                            <p class="text-muted mb-1">Total Displayed Schedules</p>
                            <h3 class="mb-0">{{ filteredSchedules.length }}</h3>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Search -->
            <div class="input-group mb-4">
                <input v-model="search" type="text" class="form-control"
                    placeholder="Search schedules..." >
                <button class="btn btn-outline-secondary" type="button"> 🔍 </button>
            </div>

            <!-- Loading -->
             <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p>Loading scheduled treks...</p>
             </div>

             <!-- Error -->
             <div v-else-if="errorMessage" class="alert alert-danger" role="alert">
                {{ errorMessage }}
                <button class="btn btn-sm btn-outline-danger ms-3" @click="getschedules">Retry</button>
             </div>

             <!-- Scheduled Treks Table -->
              <div v-else class="table-responsive">
                <table class="table table-bordered table-hover align-middle">

                    <thead class="table-light">
                        <tr>
                            <th scope="col">Schedule ID</th>
                            <th scope="col">Trek Name</th>
                            <th scope="col">Location</th>
                            <th scope="col">Assigned Staff</th>
                            <th scope="col">Trek Dates</th>
                            <th scope="col">Duration</th>
                            <th scope="col">Total slots</th>
                            <th scope="col">Available slots</th>
                            <th scope="col">Progress</th>
                            <th scope="col">Schedule Status</th>

                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="schedule in filteredSchedules" :key="schedule.availability_id">

                            <td>{{ schedule.availability_id }}</td>
                            <td>{{ schedule.trek_name }}</td>
                            <td>{{ schedule.location }}</td>
                            <td>{{ schedule.assigned_staff }}</td>
                            <td>
                                {{
                                    schedule.start_date === schedule.end_date
                                        ? $formatDate(schedule.start_date)
                                        : `${$formatDate(schedule.start_date)} - ${$formatDate(schedule.end_date)}`
                                
                                }}

                            </td>
                            <td>{{ schedule.duration }}</td>
                            
                            <td>{{ schedule.total_slot }}</td>
                            <td>
                                <span :class="schedule.avail_slot === 0
                                    ? 'text-danger fw-bold'
                                    : 'text-success fw-bold'">
                                    {{ schedule.avail_slot }}
                                </span>
                            </td>

                            
                            <td>
                                <span
                                    class="badge"
                                    :class="{
                                        'text-bg-light': schedule.progress_status == 'Not Started',
                                        'text-bg-info': schedule.progress_status == 'Ongoing',
                                        'text-bg-dark': schedule.progress_status == 'Completed',
                                    }"

                                >
                                    {{ schedule.progress_status }}
                                </span>
                            </td>

                            <td>{{ schedule.status }}</td>

                        </tr>
                    </tbody>
                </table>
              </div>
        </main>
    </div>

</template>

<script setup>
import DashNavbar from '../components/DashNavbar.vue'
import AdminSidebar from '../components/AdminSidebar.vue'

import { ref, computed, onMounted } from 'vue'

const schedules = ref([])
const search = ref('')

const loading = ref(false)
const errorMessage = ref('')


function getToday() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

const today = getToday();

async function getschedules() {
    loading.value = true
    errorMessage.value = ''

    try {
        const response = await fetch('http://127.0.0.1:5000/api/admin_dashboard/scheduled_treks', {
            headers: {
                'Authentication-Token': localStorage.getItem('auth_token')
            }
        })

        const data = await response.json()

        if (!response.ok) {
            throw new Error(data.message || 'Failed to load schedules')
        }

        if (!Array.isArray(data)) {
            throw new Error('Invalid response format')
        }

        schedules.value = data

    } catch (error) {
        console.error('Error fetching schedules: ', error)
        errorMessage.value = error.message || 'Unable to load schedules.'
    } finally {
        loading.value = false
    }
}

const filteredSchedules = computed(() => {
    const text = search.value.trim().toLowerCase()

    return schedules.value.filter(schedule => {
        const progress = schedule.progress_status
        const startDate = schedule.start_date
        const endDate = schedule.end_date

        const isUpcoming = progress === 'Not Started' && startDate >= today
        const isOngoing = progress === 'Ongoing' && startDate <= today && endDate >= today

        const matchesProgress = isUpcoming || isOngoing

        const matchesSearch =
            String(schedule.trek_name ?? '').toLowerCase().includes(text) ||
            String(schedule.location ?? '').toLowerCase().includes(text) ||
            String(schedule.assigned_staff ?? '').toLowerCase().includes(text) ||
            String(schedule.availability_id ?? '').includes(text)

        return matchesProgress && matchesSearch
    }).sort((a, b) => {
        return a.start_date.localeCompare(b.start_date)
    })
})

const ongoingCount = computed(() => {
    return filteredSchedules.value.filter(schedule => schedule.progress_status === 'Ongoing').length
})

const upcomingCount = computed(() => {
    return filteredSchedules.value.filter(schedule => schedule.progress_status === 'Not Started').length
})


function formatDate(value) {
    if (!value) return '-'

    const [year, month, day] = value.split('-')
    return `${day}/${month}/${year}`
}



onMounted(() => {
    getschedules()
})
</script>