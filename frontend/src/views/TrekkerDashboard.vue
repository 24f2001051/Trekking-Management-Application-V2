<template>
    <DashNavbar />

    <div class="d-flex">
        <TrekkerSidebar />

        <main class="flex-grow-1 p-4">
            <h1>TREKKER DASHBOARD</h1>
            <br>
            
            <!-- OR your dashboard cards -->
        
        <div class="row g-3 mb-4">

            <div class="col-12 col-sm-6 col-xl-3">
                <div class="card summary-card h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <p class="text-muted mb-1">Available Treks</p>
                                <h3 class="fw-bold">{{ availableTreks.length }}</h3>
                            </div>
                            <span class="summary-icon">🥾</span>
                        </div>
                        <RouterLink
                            to="/trekker_dashboard/browse_trek"
                            class="small text-decoration-none">Explore Treks →
                        </RouterLink>
                    </div>
                </div>
            </div>

            <div class="col-12 col-sm-6 col-xl-3">
                <div class="card summary-card h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <p class="text-muted mb-1">Total Bookings</p>
                                <h3 class="fw-bold">{{ totalBookings }}</h3>
                            </div>
                            <span class="summary-icon">📋</span>
                        </div>
                        
                    </div>
                </div>
            </div>

            <div class="col-12 col-sm-6 col-xl-3">
                <div class="card summary-card h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <p class="text-muted mb-1">Upcoming Booked Treks</p>
                                <h3 class="fw-bold">{{ upcomingBookings }}</h3>
                            </div>
                            <span class="summary-icon">📅</span>
                        </div>
                        <RouterLink
                            to="/trekker_dashboard/my_booking"
                            class="small text-decoration-none">View bookings →
                        </RouterLink>
                    </div>
                </div>
            </div>

            <div class="col-12 col-sm-6 col-xl-3">
                <div class="card summary-card h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <p class="text-muted mb-1">Completed Treks</p>
                                <h3 class="fw-bold">{{ completedTreks }}</h3>
                            </div>
                            <span class="summary-icon">🏆</span>
                        </div>
                        <RouterLink
                            to="/trekker_dashboard/history"
                            class="small text-decoration-none">View history →
                        </RouterLink>
                    </div>
                </div>
            </div>
        </div>
        <br>
        
        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2">Loading your dashboard...</p>
        </div>
        
        <div v-else-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
            <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchDashboard">
                Retry
            </button>
        </div>
        
        <template v-else>

            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="fw-bold mb-0">Available Treks</h4>
                <RouterLink to="/trekker_dashboard/browse_trek" class="btn btn-outline-primary btn-sm">
                    View All
                </RouterLink>
            </div>

            <div v-if="availableTreks.length === 0" class="alert alert-info">
                No treks are currently available for booking.
            </div>

            <div v-else class="row g-3 mb-5">
                <div v-for="trek in availableTreks.slice(0, 3)" :key="trek.trek_id" class="col-12 col-md-6 col-xl-4">
                    
                    <div class="card trek-card h-100">
                        <div class="trek-image">
                            <img 
                                v-if="trek.image_url"
                                :src="trek.image_url"
                                :alt="trek.trek_name"
                            />
                            <div v-else class="trek-placeholder">
                                <span>🏔️</span>
                                <small>{{ trek.trek_name }}</small>
                            </div>
                        </div>

                        <div class="card-body">
                            <h5 class="fw-bold">{{ trek.trek_name }}</h5>

                            <p class="text-muted mb-2">
                                📍 {{ trek.location || 'Location not specified' }}
                                <span class="ms-5 badge bg-primary">{{ trek.difficulty || 'Not specified' }}</span>
                                <span class="ms-5 text-muted">{{ trek.duration }} days</span>
                            </p>

                            <p class="mb-3">
                                <strong>Slots left:</strong>
                                {{ trek.avail_slot }}
                            </p>

                            <button
                                class="btn btn-primary w-100"
                                :disabled="Number(trek.avail_slot) <= 0"
                                @click="openTrek(trek)">
                                {{
                                    Number(trek.avail_slot) > 0
                                        ? 'Booking Available'
                                        : 'Not Available'
                                }}
                            </button>
                        </div>

                    </div>
                </div>
            </div>

            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="fw-bold mb-0">My Recent Bookings</h4>
                <RouterLink
                    to="/trekker_dashboard/my_booking" class="btn btn-outline-primary btn-sm">
                    View All
                </RouterLink>
            </div>

            <div class="card border-0 shadow-sm">
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th>Trek Name</th>
                                <th>Booking Date</th>
                                <th>Trek Dates</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="booking in recentBookings" :key="booking.booking_id">
                                <td>{{ booking.trek_name }}</td>
                                <td>{{ $formatDate(booking.booking_date) }}</td>
                                <td>
                                    {{
                                        booking.start_date === booking.end_date
                                            ? $formatDate(booking.start_date)
                                            : `${$formatDate(booking.start_date)} - ${$formatDate(booking.end_date)}`
                                    }}

                                </td>
                                <td>
                                    <span
                                        class="badge"
                                        :class="{
                                            'text-bg-primary': booking.booking_status == 'Booked',
                                            'text-bg-danger': booking.booking_status == 'Cancelled',
                                            'text-bg-success': booking.booking_status == 'Completed',
                                        }"
                                    >                                        
                                        {{ booking.booking_status }}
                                    </span>
                                    <span
                                        v-if="
                                            booking.booking_status !== 'Cancelled' &&
                                            !(booking.booking_status === 'Completed' &&
                                            booking.progress_status === 'Completed')
                                        "
                                        class="badge ms-3"
                                        :class="{
                                            'text-bg-light': booking.progress_status == 'Not Started',
                                            'text-bg-info': booking.progress_status == 'Ongoing',
                                            'text-bg-dark': booking.progress_status == 'Completed',
                                        }"
                                    >
                                        {{ booking.progress_status || 'N/A' }}
                                    </span>
                                    <span
                                        v-else-if="booking.booking_status === 'Cancelled'"
                                        class="text-muted"
                                    >
                                        -
                                    </span>

                                </td>
                                <td>
                                    <RouterLink
                                        to="/trekker_dashboard/my_booking"
                                        class="btn btn-sm btn-outline-primary">
                                        View
                                    </RouterLink>
                                </td>
                            </tr>

                            <tr v-if="recentBookings.length === 0">
                                <td colspan="5" class="text-center py-4">No recent bookings found.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </template>
        </main>
    </div>
</template>





<script setup>
import DashNavbar from '../components/DashNavbar.vue'
import TrekkerSidebar from '../components/TrekkerSidebar.vue';
import { useRouter, RouterLink } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
const router = useRouter();

const fullname = localStorage.getItem('fullname') || 'Trekker';

const availableTreks = ref([]);
const recentBookings = ref([]);
const loading = ref(false);
const errorMessage = ref('');

const totalBookings = computed(() =>
    recentBookings.value.filter(booking => booking.booking_status !== 'Cancelled').length
);

const upcomingBookings = computed(() =>
    recentBookings.value.filter(booking =>
        String(booking.booking_status || '').toLowerCase() === 'booked'
    ).length
);

const completedTreks = computed(() =>
    recentBookings.value.filter(booking =>
        String(booking.booking_status || '').toLowerCase() === 'completed'
    ).length
);

async function fetchDashboard() {
    loading.value = true
    errorMessage.value = ''

    try {
        const token = localStorage.getItem('auth_token')

        if (!token) {
            router.push('/login')
            return
        }

        const response = await fetch('http://127.0.0.1:5000/api/trekker_dashboard', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            }
        })

        if (response.status === 401 || response.status === 403) {
            errorMessage.value = 'Your session may have expired. Please log in again.'
            return
        }

        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`)
        }

        const data = await response.json()

        availableTreks.value = data.available_treks || []
        recentBookings.value = data.recent_bookings || []

    } catch (error) {
        console.error('Error loading trekker dashboard:', error)
        errorMessage.value = 'Unable to load dashboard data. Check whether the Flask backend is running.'
    } finally {
        loading.value = false
    }
}

function openTrek(trek) {
    router.push({
        path: '/trekker_dashboard/browse_trek',
        query: { trek_id: trek.trek_id }
    })
}

function formatDate(date) {
    if (!date) return '-'

    if (/^\d{2}-\d{2}-\d{4}$/.test(date)) {
        return date
    }

    const match = String(date).match(/^(\d{4})-(\d{2})-(\d{2})$/)

    if (match) {
        return `${match[3]}-${match[2]}-${match[1]}`
    }
    return date
}

function statusClass(status) {
    switch (String(status || '').toLowerCase()) {
        case 'booked':
        case 'confirmed':
            return 'bg-success'
        case 'completed':
            return 'bg-primary'
        case 'cancelled':
        case 'rejected':
            return 'bg-danger'
        default:
            return 'bg-secondary'
    }
}

onMounted(fetchDashboard)

</script>

<style scoped>
.trekker-layout {
    min-height: calc(100vh - 60px);
}

.dashboard-content {
    min-width: 0;
    background: #f8fafc;
}

.summary-card {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.summary-icon {
    font-size: 1.8rem;
}

.trek-card {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.trek-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 16px rgba(0, 0, 0, 0.08);
}

.trek-image {
    height: 170px;
    background: #e5edf6;
}

.trek-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.trek-placeholder {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 8px;
    color: #315780;
}

.trek-placeholder span {
    font-size: 3rem;
}

.table th,
.table td {
    white-space: nowrap;
}

@media (max-width: 768px) {
    .dashboard-content {
        padding: 1rem !important;
    }
}
</style>