<template>
    <DashNavbar />

    <div class="d-flex">
        <TrekkerSidebar />

        <main class="flex-grow-1 p-4">
            <h2 calss="fw-bold">My Bookings</h2>
            <p class="text-muted mb-4">Manage your booked trekking schedules.</p>

            <div v-if="message" class="alert" :class="messageType === 'success' ? 'alert-success' : 'alert-danger'">
                {{ message }}
            </div>
            
            <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary"></div>
                <p>Loading bookings...</p>
            </div>

            <div v-else-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
                <button class="btn btn-sm btn-outline-danger ms-2" @click="loadBookings">Retry</button>
            </div>

            <div v-else class="card border-0 shadow-sm">
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th scope="col">Trek</th>
                                <th scope="col">Location</th>
                                <th scope="col">Booking Date</th>
                                <th scope="col">Trek Date</th>
                                <th scope="col">Progress</th>
                                <th scope="col">Status</th>
                                <th scope="col">Actions</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="booking in bookings" :key="booking.booking_id">
                                <td class="fw-semibold">{{ booking.trek_name }}</td>
                                <td>{{ booking.location }}</td>
                                <td>{{ booking.booking_date }}</td>
                                <td>
                                    {{ booking.start_date || '-' }}
                                    <span v-if="booking.end_date">
                                        - {{ booking.end_date }}
                                    </span>
                                </td>
                                <td>{{ booking.progress_status }}</td>
                                <td>
                                    <span class="badge bg-success">{{ booking.status }}</span>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-outline-danger"
                                        :disabled="cancellingID === booking.booking_id" @click="cancelBooking(booking)">
                                        {{
                                            cancellingID === booking.booking_id
                                            ? 'Cancelling...'
                                            : 'Cancel'
                                        }}
                                    </button>
                                </td>
                            </tr>

                            <tr v-if="bookings.length === 0">
                                <td colspan="7" class="text-center py-5">
                                    <h5>No active bookings yet!</h5>
                                    <p class="text-muted">Explore the available treks to get started.</p>
                                    <RouterLink to="/trekker_dashboard/browse_trek" class="btn btn-primary">
                                        Browse Treks
                                    </RouterLink>
                                </td>
                            </tr>

                        </tbody>
                    </table>
                </div>
            </div>
        
        </main>
    </div>

</template>



<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import DashNavbar from '../components/DashNavbar.vue';
import TrekkerSidebar from '../components/TrekkerSidebar.vue';

const router = useRouter();

const bookings = ref([]);
const loading = ref(false);
const errorMessage = ref('');
const message = ref('');
const messageType = ref('success');
const cancellingID = ref(null);

async function loadBookings() {
    loading.value = true;
    errorMessage.value = '';

    try {
        const token = localStorage.getItem('auth_token');

        if (!token) {
            router.push('/login');
            return;
        }

        const response = await fetch('http://127.0.0.1:5000/api/trekker_dashboard/my_booking', {
            method: 'GET',
            headers: {
                'Authentication-Token': token
            }
        });

        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }

        const data = await response.json();

        const bookingList = Array.isArray(data)
            ? data
            : Array.isArray(data.bookings)
                ? data.bookings
                : [];

        bookings.value = bookingList.filter(booking =>
            booking &&
            booking.booking_id != null &&
            booking.trek_name
        );
    
    } catch (error) {
        console.error('Bookings API error:', error);
        errorMessage.value = error.message || 'Unable to load bookings';
    } finally {
        loading.value = false;
    }
}

async function cancelBooking(booking) {

    const confirmed = confirm(`Cancel your booking for ${booking.trek_name}?`);

    if (!confirmed) return;

    cancellingID.value = booking.booking_id;

    try {
        const token = localStorage.getItem('auth_token');
        if (!token) {
            throw new Error('Please log in again.');
        }

        const response = await fetch(`http://127.0.0.1:5000/api/trekker_dashboard/my_booking/${booking.booking_id}/cancel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Cancellation failed.');
        }

        message.value = data.message || 'Booking cancelled successfully';
        messageType.value = 'success';

        await loadBookings();

    } catch (error) {
        message.value = error.message || 'Unable to cancel booking.';
        messageType.value = 'error';
    } finally {
        cancellingID.value = null;
    }
}

onMounted(() => {
    loadBookings();
});

</script>


<style scoped>
.trekker-layout {
    min-height: calc(100vh - 60px);
}

.dashboard-content {
    min-width: 0;
    background: #f8fafc;
}

.card {
    border-radius: 12px;
    overflow: hidden;
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