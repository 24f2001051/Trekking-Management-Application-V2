<template>
    <DashNavbar />

    <div class="d-flex">
        <TrekkerSidebar />

        <main class="flex-grow-1 p-4">
            <h2 class="fw-bold">My Trekking History</h2>
            <p class="text-muted mb-4">Review your completed and cancelled treks.</p>

            <div class="row g-3 mb-4">
                <div class="col-12 col-md-6">
                    <div class="card history-stat">
                        <div class="card-body">
                            <p class="text-muted mb-1">Completed Treks</p>
                            <h3 class="fw-bold">{{ completedCount }}</h3>
                        </div>
                    </div>
                </div>

                <div class="col-12 col-md-6">
                    <div class="card history-stat">
                        <div class="card-body">
                            <p class="text-muted mb-1">Cancelled Treks</p>
                            <h3 class="fw-bold">{{ cancelledCount }}</h3>
                        </div>
                    </div>
                </div>
            </div>

            <div class="d-flex flex-wrap gap-2 mb-3">
                <button v-for="option in filters"
                    :key="option.value" class="btn btn-sm"
                    :class="filter === option.value
                        ? 'btn-outline-primary' : 'btn-outline-secondary'"
                    @click="filter = option.value">
                    {{ option.label }}
                </button>
            </div>

            <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary"></div>
                <p>Loading history...</p>
            </div>

            <div v-else-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
                <button class="btn btn-sm btn-outline-danger ms-2" @click="loadHistory">Retry</button>
            </div>

            <div v-else class="card border-0 shadow-sm">
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th scope="col">Trek Name</th>
                                <th scope="col">Location</th>
                                <th scope="col">Trek Dates</th>
                                <th scope="col">Booking Date</th>
                                <th scope="col">Progress</th>
                                <th scope="col">Status</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="item in filteredHistory" :key="item.booking_id">
                                <td class="fw-semibold">{{ item.trek_name }}</td>
                                <td>{{ item.location }}</td>
                                <td>
                                    {{ item.start_date || '-' }}
                                    <span v-if="item.end_date"> - {{ item.end_date }}</span>
                                </td>
                                <td>{{ item.booking_date }}</td>
                                <td>{{ item.progress_status }}</td>
                                <td>
                                    <span class="badge" :class="item.status === 'Completed' ? 'bg-success' : 'bg-danger'">
                                        {{ item.status }}
                                    </span>
                                </td>
                            </tr>

                            <tr v-if="filteredHistory.length === 0">
                                <td colspan="6" class="text-center py-5">No records found for this filter.</td>
                            </tr>

                        </tbody>
                    </table>
                </div>
            </div>


        </main>
    </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue';
import TrekkerSidebar from '../components/TrekkerSidebar.vue';
import DashNavbar from '../components/DashNavbar.vue';
import { useRouter } from 'vue-router'; // 1. Import it
const router = useRouter(); // 2. Define it

const history = ref([]);
const loading = ref(false);
const errorMessage = ref('');
const filter = ref('all');

const filters = [
    { label: 'All History', value: 'all' },
    { label: 'Completed', value: 'Completed' },
    { label: 'Cancelled', value: 'Cancelled' },
];

const completedCount = computed(() => history.value.filter(item => item.status === 'Completed').length);
const cancelledCount = computed(() => history.value.filter(item => item.status === 'Cancelled').length);

const filteredHistory = computed(() => {
    if (filter.value === 'all') {
        return history.value;
    } else {
        return history.value.filter(item => item.status === filter.value);
    }
});

async function loadHistory() {
    loading.value = true;
    errorMessage.value = '';

    try {
        const token = localStorage.getItem('auth_token');

        if (!token) {
            router.push('/login');
            return;
        }

        const response = await fetch(
            'http://127.0.0.1:5000/api/trekker_dashboard/history',
            {
                method: 'GET',
                headers: {
                    'Authentication-Token': token
                }
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || `Request failed: ${response.status}`);
        }

        history.value = Array.isArray(data.result) ? data.result : [];

    } catch (error) {
        console.error('History API error:', error);
        errorMessage.value = error.message || 'Unable to load trekking history.';
    } finally {
        loading.value = false;
    }
}

onMounted(() => {
    loadHistory();
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

.history-stat {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
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