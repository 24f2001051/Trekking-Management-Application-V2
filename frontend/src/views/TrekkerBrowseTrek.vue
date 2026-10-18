<template>
    <DashNavbar />

    <div class="d-flex">
        <TrekkerSidebar />

        <main class="flex-grow-1 p-4">
            <h2 class="fw-bold">Browse Treks</h2>
            <p class="text-muted">Discover your next adventure and choose an available schedule.</p>

            <div class="card border-0 shadow-sm p-3 mb-4">
                <div class="row g-2 align-items-end">
                    <div class="col-12 col-md-5">
                        <label class="form-label small mb-1">Search Trek</label>
                        <input v-model="search" class="form-control form-control-sm"
                            placeholder="Search trek or location..." @input="applyFilters">
                    </div>

                    <div class="col-6 col-md-3">
                        <label class="form-label small mb-1">Difficulty</label>
                        <select v-model="difficulty" class="form-select form-select-sm" @change="applyFilters">
                            <option value="">All</option>
                            <option value="Explorer">Explorer (Beginner)</option>
                            <option value="Adventurer">Adventurer (Intermediate)</option>
                            <option value="Trailblazer">Trailblazer (Advanced)</option>
                        </select>
                    </div>

                    <div class="col-6 col-md-2">
                        <label class="form-label small mb-1">Duration (in days)</label>
                        <input v-model="duration" class="form-control form-control-sm" placeholder="e.g. 4 days" @input="applyFilters">
                    </div>

                    <div class="col-6 col-md-2">
                        <button type="button" class="btn btn-outline-secondary w-100"
                            @click="resetFilters">Reset Filters</button>
                    </div>

                </div>
            </div>

            <!-- ------------------------------------------------------- -->

            <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary"></div>
                <p class="mt-2">Loading available treks...</p>
            </div>

            <div v-else-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
                <button class="btn btn-sm btn-outline-danger ms-2" @click="loadTreks">Retry</button>
            </div>

            <div v-else-if="treks.length === 0" class="alert alert-info">
                No matching treks with available schedules were found.
            </div>

            <div v-else class="row g-4">
                <div v-for="trek in treks" :key="trek.trek_id" class="col-12 col-md-6 col-xl-4">
                    <div class="card trek-card h-100">

                        <div class="trek-image"> <span>🏔️</span> </div>

                        <div class="card-body">
                            <h5 class="fw-bold">{{ trek.trek_name }}</h5>


                            <div class="d-flex justify-content-between align-items-center gap-2 mb-2">
                                <p class="text-muted mb-2 text-truncate">📍 {{ trek.location }}</p>

                                <span class="badge bg-primary flex-shrink-0">{{ trek.difficulty }}</span>
                            </div>
                            
                            <p class="mt-3 mt-2"><strong>Duration:</strong> {{ trek.duration }} days</p>

                            <div class="description mb-3">
                                <strong>Description:</strong>
                                <span :class="{ 'description-collapsed': !expandedDescriptions[trek.trek_id] }">
                                    {{ trek.description || 'No description available.' }}
                                </span>

                                <button
                                    v-if="trek.description && trek.description.length > 80" type="button"
                                    class="btn btn-link btn-sm p-0 ms-1" @click="toggleDescription(trek.trek_id)">
                                    {{ expandedDescriptions[trek.trek_id] ? 'Show less ▵' : 'Show more ▿' }}
                                </button>

                            </div>

                            <hr>

                            <label class="form-label fw-semibold">Select Trek Dates</label>

                            <select v-model="selectedSchedules[trek.trek_id]" class="form-select mb-3">
                                <option v-for="schedule in trek.schedules" :key="schedule.availability_id" :value="schedule.availability_id">
                                    {{ schedule.start_date }} - {{ schedule.end_date }}
                                    ({{ schedule.avail_slot }} slots left)
                                </option>
                            </select>

                            <div v-if="getSelectedSchedule(trek)" class="small text-muted mb-3">
                                <div>Total slots: {{ getSelectedSchedule(trek).total_slot }}</div>
                                <div>Available: {{ getSelectedSchedule(trek).avail_slot }}</div>
                            </div>

                            <button
                                class="btn btn-primary w-100"
                                :disabled="
                                    !getSelectedSchedule(trek) ||
                                    Number(getSelectedSchedule(trek).avail_slot) <= 0 ||
                                    bookingId === trek.trek_id
                                "
                                @click="bookTrek(trek)">
                                {{
                                    bookingId === trek.trek_id
                                        ? 'Booking...'
                                        : 'Book This Trek'
                                }}
                            </button>

                        </div>

                    </div>
                </div>
            </div>


        </main>
    </div>

</template>


<script setup>
import TrekkerSidebar from '../components/TrekkerSidebar.vue';
import DashNavbar from '../components/DashNavbar.vue'
import { ref, computed, onMounted, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const treks = ref([]);
const loading = ref(false);
const errorMessage = ref('');
const bookingId = ref(null);

const search = ref('');
const location = ref('');
const duration = ref('');
const difficulty = ref('');

const selectedSchedules = reactive({});
const expandedDescriptions = reactive({});

let filterTimer = null

async function loadTreks() {
    loading.value = true;
    errorMessage.value = '';

    try {
        const token = localStorage.getItem('auth_token');

        if (!token) {
            await router.push('/login');
            return;
        }

        const params = new URLSearchParams();

        if (search.value.trim()) {
            params.set('search', search.value.trim())
        }
        if (location.value.trim()) {
            params.set('location', location.value.trim())
        }
        if (duration.value.trim()) {
            params.set('duration', duration.value.trim())
        }
        if (difficulty.value) {
            params.set('difficulty', difficulty.value);
        }

        const response = await fetch(`http://127.0.0.1:5000/api/trekker_dashboard/browse_trek?${params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            }
        })

        const data = await response.json()

        if (!response.ok) {
            throw new Error(data.message || `Request failed: ${response.status}`);
        }

        if (!Array.isArray(data.treks)) {
            throw new Error(data.message || 'Invalid response: expected a treks array.');
        }

        treks.value = data.treks.map(trek => ({
            ...trek,
            schedules: Array.isArray(trek.schedules)
                ? trek.schedules
                : Array.isArray(trek.schedule)
                    ? trek.schedule
                    : []
        }));
    

        for (const trek of treks.value) {
            const schedules = trek.schedules;
            const currentId = Number(selectedSchedules[trek.trek_id]);


            if (
                !schedules.some(
                    item => Number(item.availability_id) === currentId
                )
            ) {
                selectedSchedules[trek.trek_id] = schedules[0]?.availability_id ?? ''
            }
        }

        if (route.query.trek_id) {
            const requestedTrek = treks.value.find(item => Number(item.trek_id) === Number(route.query.trek_id));
            if (requestedTrek) {
                document.
                getElementById(`trek-${requestedTrek.trek_id}`)
                ?.scrollIntoView({ behavior: 'smooth' });
            }
        }

    } catch (error) {
        console.error('Error loading treks:', error)
        errorMessage.value = error.message || 'Unable to load treks. Check the flask backend';
    } finally {
        loading.value = false;
    }
}


function applyFilters() {
    clearTimeout(filterTimer);
    filterTimer = setTimeout(loadTreks, 300);
}
function resetFilters() {
    search.value = '';
    location.value = '';
    duration.value = '';
    difficulty.value = '';
    loadTreks();
}
function getSelectedSchedule(trek) {
    return trek.schedules.find(schedule => schedule.availability_id === Number(selectedSchedules[trek.trek_id]));
}

function toggleDescription(trekId) {
    expandedDescriptions[trekId] = !expandedDescriptions[trekId];
}

async function bookTrek(trek) {
    const schedule = getSelectedSchedule(trek);

    if (!schedule) {
        alert('Please select a schedule before booking.');
        return;
    }
    if (Number(schedule.avail_slot) <= 0) {
        alert('No more slots available for this schedule.');
        await loadTreks();
        return;
    }

    if (!confirm(`Book ${trek.trek_name} from ${schedule.start_date} to ${schedule.end_date}?`)) {
        return;
    }

    bookingId.value = trek.trek_id;

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/trekker_dashboard/treks/${trek.trek_id}/book`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth_token')
            },
            body: JSON.stringify({
                availability_id: schedule.availability_id
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.message || 'Booking failed.');
            await loadTreks();
            return;
        }

        alert(data.message || 'Trek booked successfully.');
        await router.push('/trekker_dashboard/my_booking');
    
    
    } catch (error) {
        console.error(error);
        alert('Unable to book the trek. Please try again.');
    } finally {
        bookingId.value = null;
    }
}



onMounted(() => {
    loadTreks();
});
</script>




<style scoped>
.trek-card {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.trek-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

.trek-image {
    height: 145px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #e5edf6;
    font-size: 4rem;
}

.description {
    min-height: 45px;
    color: #6c757d;
    line-height: 1.5;
    overflow-wrap: anywhere; 
}

.description-collapsed {
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.description button {
    text-decoration: None;
    white-space: nowrap;
}

@media (max-width: 768px) {
    .dashboard-content {
        padding: 1rem !important;
    }
}
</style>

