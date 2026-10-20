<template>
    <DashNavbar />

    <div class="d-flex">
        <StaffSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Manage Trek Schedule</h2>
                <button class="btn btn-outline-secondary" @click="goBack">
                    Back to Dashboard
                </button>
            </div>

            <div v-if="loading" class="text-center p-4">
                Loading trek schedule...
            </div>

            <div v-else-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
            </div>

            <div v-else-if="schedule" class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">{{ schedule.trek_name }}</h4>
                </div>

                <div class="card-body">
                    <p><strong>Location:</strong> {{ schedule.location }}</p>
                    <p><strong>Dates:</strong> {{ schedule.dates }}</p>
                    <p><strong>Total slots:</strong> {{ schedule.total_slot }}</p>
                    <p><strong>Booked participants:</strong> {{ bookedCount }}</p>

                    <p>
                        <strong>Booking status:</strong>
                        <span class="badge ms-2"
                            :class="schedule.status === 'Open'
                                ? 'bg-success' : 'bg-danger'">
                            {{ schedule.status }}
                        </span>
                    </p>

                    <p>
                        <strong>Trek progress:</strong>
                        <span class="badge ms-2"
                            :class="{
                                'bg-secondary': schedule.progress_status === 'Not Started',
                                'bg-info': schedule.progress_status === 'Ongoing',
                                'bg-success': schedule.progress_status === 'Completed'
                            }">
                            {{ schedule.progress_status }}
                        </span>
                    </p>

                    <hr>

                    <form @submit.prevent="saveSchedule">
                        <div class="row g-3 mb-3">

                            <div class="col-md-4">
                                <label for="avail_slot" class="form-label">
                                    Available slots
                                </label>

                                <input
                                    id="avail_slot"
                                    v-model.number="form.avail_slot"
                                    type="number"
                                    class="form-control"
                                    min="0"
                                    :max="schedule.total_slot - bookedCount"
                                    :disabled="!canManage || schedule.status === 'Closed'"
                                    required
                                >

                                <small class="text-muted">
                                    Maximum available slots:
                                    {{ schedule.total_slot - bookedCount }}
                                </small>
                            </div>
                        

                            <div class="col-md-4">
                                <label for="booking_status" class="form-label">
                                    Booking Status
                                </label>

                                <select
                                    id="booking_status"
                                    v-model="form.status"
                                    class="form-select"
                                    :disabled="!canManage"
                                >
                                    <option value="Open">Open</option>
                                    <option value="Closed">Closed</option>
                                </select>
                            </div>

                            <div class="col-md-4">
                                <label for="progress_status" class="form-label">
                                    Progress Status
                                </label>

                                <select
                                    id="progress_status"
                                    v-model="form.progress_status"
                                    class="form-select"
                                    :disabled="!canManage"
                                    @change="handleProgressChange"
                                >
                                    <option value="Not Started">Not Started</option>
                                    <option value="Ongoing">Ongoing</option>
                                    <option value="Completed">Completed</option>
                                </select>
                            </div>




                        </div>

                        <div v-if="!canManage" class="alert alert-warning">
                            This schedule has started or completed, or its
                            trek is inactive. Booking settings cannot be changed.
                        </div>

                        <div v-if="message" class="alert alert-success">
                            {{ message }}
                        </div>

                        <div v-if="saveError" class="alert alert-danger">
                            {{ saveError }}
                        </div>

                        <button
                            v-if="canManage"
                            type="submit"
                            class="btn btn-primary"
                            :disabled="saving"
                        >
                            {{ saving ? 'Saving...' : 'Save Changes' }}
                        </button>
                    </form>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import DashNavbar from '@/components/DashNavbar.vue';
import StaffSidebar from '@/components/StaffSidebar.vue';

const API = 'http://127.0.0.1:5000/api';

const route = useRoute();
const router = useRouter();

const loading = ref(true);
const saving = ref(false);
const errorMessage = ref('');
const saveError = ref('');
const message = ref('');
const schedule = ref(null);

const form = ref({
    avail_slot: 0,
    status: 'Closed',
    progress_status: 'Not Started',
});

const bookedCount = computed(() =>
    Math.max(0, schedule.value.total_slot - schedule.value.avail_slot)
);

const canManage = computed(() => {
    if (!schedule.value) return false;

    return schedule.value.progress_status !== 'Completed';
});

function goBack() {
    router.push('/staff_dashboard');
}


function handleProgressChange() {
    if (
        form.value.status === 'Ongoing' || form.value.progress_status === 'Completed'
    ) {
        form.value.status = 'Closed';
    }
}





async function getSchedule() {
    loading.value = true;
    errorMessage.value = '';

    try {
        const token = localStorage.getItem('auth_token');

        if (!token) {
            throw new Error('Please log in again.');
        }

        const response = await fetch(
            `${API}/staff_dashboard/my_trek`,
            {
                headers: {
                    'Authentication-Token': token
                }
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Unable to load trek.');
        }

        const trekId = Number(route.query.trek_id);
        const availabilityId = Number(route.query.availability_id);

        if (Number(data.trek.trek_id) !== trekId) {
            throw new Error('This trek is not assigned to you.');
        }

        const selected = data.schedules.find(
            item => Number(item.availability_id) === availabilityId
        );

        if (!selected) {
            throw new Error('The selected trek schedule was not found.');
        }

        schedule.value = {
            ...selected,
            location: data.trek.location,
            trek_id: data.trek.trek_id
        };

        form.value.avail_slot = selected.avail_slot;
        form.value.status = selected.status;
        form.value.progress_status = selected.progress_status;
    } catch (error) {
        errorMessage.value = error.message || 'Unable to load schedule.';
    } finally {
        loading.value = false;
    }
}

async function saveSchedule() {
    saving.value = true;
    saveError.value = '';
    message.value = '';

    try {
        const token = localStorage.getItem('auth_token');

        const response = await fetch(
            `${API}/staff_dashboard/availability/${schedule.value.availability_id}`,
            {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': token
                },
                body: JSON.stringify({
                    avail_slot: form.value.avail_slot,
                    status: form.value.status,
                    progress_status: form.value.progress_status
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Unable to update schedule.');
        }

        message.value = data.message || 'Schedule updated successfully.';

        await getSchedule();
    } catch (error) {
        saveError.value = error.message || 'Unable to save changes.';
    } finally {
        saving.value = false;
    }
}

onMounted(getSchedule);
</script>
