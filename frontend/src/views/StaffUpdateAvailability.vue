<template>
    <DashNavbar />

    <div class="d-flex">
        <StaffSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Update Trek Schedule</h2>
                <button class="btn btn-outline-secondary" @click="goBack" > Back to My Trek </button>
            </div>

            <div v-if="errorMessage" class="alert alert-danger"> {{ errorMessage }} </div>
            <div v-if="errorMessage" class="alert alert-danger"> {{ successMessage }} </div>

            <div v-if="loading" class="text-center p-4"> Loading schedule... </div>

           
            <div v-else-if="schedule" class="card shadow-sm mb-4">
                <div class="card-header bg-white">
                    <h4 class="mb-0"> {{ schedule.trek_name }} </h4>
                    <small class="text-muted">Schedule: {{ schedule.date }} </small>
                </div>

                <div class="card-body p-4">

                    <form @submit.prevent="saveChanges">
                        <div class="mb-3">
                            <label for="totalSlots" class="form-label">Total Slot Capacity:</label>

                            <input id="totalSlots" type="number" class="form-control"
                            :value="schedule.total_slot" disabled/>

                            <small class="text-muted">
                                Total capacity is fixed for this schedule.
                            </small>
                        </div>

                        <div class="mb-3">
                            <label for="availableSlots" class="form-label">Available Slots:</label>

                            <input id="availableSlots" type="number" class="form-control"
                            v-model.number="form.avail_slot" min="0" :max="schedule.total_slot" required/>

                            <small class="text-muted">
                                Current capacity: {{ schedule.total_slot }}.
                            </small>
                        </div>

                        <div class="mb-3">
                            <label for="bookingStatus" class="form-label">Booking Status:</label>

                            <select class="form-select" id="bookingStatus" v-model="form.status" required>
                                <option value="Open">Open</option>
                                <option value="Closed">Closed</option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="progressStatus" class="form-label">Trek Progress:</label>

                            <select class="form-select" id="progressStatus" v-model="form.progress_status" required>
                                <option value="Not Started">Not Started</option>
                                <option value="Ongoing">Ongoing</option>
                                <option value="Completed">Completed</option>
                            </select>
                        </div>

                        <button type="submit" class="btn btn-primary" :disabled="saving">
                            {{ saving ? 'Saving...' : 'Save Changes' }}
                        </button>

                    </form>

                </div>
            </div>

            <div v-else-if="!loading" class="alert alert-warning">
                Schedule not found. Return to My trek and select a schedule.
            </div>

        </main>
    </div>

</template>

<script setup>

import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import DashNavbar from '@/components/DashNavbar.vue';
import StaffSidebar from '@/components/StaffSidebar.vue';

const route = useRoute();
const router = useRouter();

const API = 'http://127.0.0.1:5000/api';

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const schedule = ref(null);
const saving = ref(false);

const form = ref({
    avail_slot: 0,
    status: 'Open',
    progress_status: 'Not Started',
});

async function getSchedule() {
    loading.value = true;
    errorMessage.value = '';
    successMessage.value = '';

    try {
        const token = localStorage.getItem('auth_token');
        const availabilityId = route.query.availability_id;

        if (!token) {
            throw new Error('Please log in again.');
        }

        if (!availabilityId) {
            throw new Error('No schedule was selected.');
        }

        const response = await fetch(`${API}/staff_dashboard/my_trek`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            }
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to fetch schedules.');
        }

        const selectedSchedule = (data.schedules || []).find(
            item => String(item.availability_id) === String(availabilityId)
        )

        if (!selectedSchedule) {
            throw new Error('Schedule not found among your assigned trek schedules.');
        }

        schedule.value = selectedSchedule;

        form.value = {
            avail_slot: selectedSchedule.avail_slot,
            status: selectedSchedule.status || 'Open',
            progress_status: selectedSchedule.progress_status || 'Not Started',
        };

    } catch (error) {
        errorMessage.value = error.message;
    } finally {
        loading.value = false;
        }
}

async function saveChanges() {
    errorMessage.value = '';
    successMessage.value = '';
    
    const availableSlots = Number(form.value.avail_slot);
    const totalSlots = Number(schedule.value.total_slot);

    if (
        !Number.isInteger(availableSlots) ||
        availableSlots < 0 ||
        availableSlots > totalSlots
    ) {
        errorMessage.value = `Available slots must be a valid integer between 0 and ${totalSlots}.`;
        return;
    }

    if (form.value.status === 'Open' && availableSlots === 0) {
        errorMessage.value = 'A schedule cannot be Open when no slots are available.';
        return;
    }

    saving.value = true;

    try {
        const token = localStorage.getItem('auth_token');
        const availabilityId = route.query.availability_id;

        const response = await fetch(`${API}/staff_dashboard/availability/${availabilityId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({
                availability_id: availabilityId,
                avail_slot: availableSlots,
                status: form.value.status,
                progress_status: form.value.progress_status
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to update schedule.');
        }

        successMessage.value = data.message || 'Schedule updated successfully.';

        await getSchedule();

    } catch (error) {
        errorMessage.value = error.message;
    } finally {
        saving.value = false;
    }
}

function goBack() {
    router.push('/staff_dashboard/my_trek');
}

onMounted(getSchedule);

</script>