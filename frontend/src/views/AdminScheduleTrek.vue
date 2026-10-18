<template>
    <DashNavbar />

    <div class="d-flex">
        <AdminSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-4">
                <h2>Schedule Trek</h2>
                <RouterLink
                    to="/admin_dashboard/treks" class="btn btn-outline-primary">
                        Go back to Treks
                </RouterLink>
            </div>

            <div v-if="loading" class="text-center py-4">Loading trek details...</div>

            <div v-else-if="errorMessage && !trek" class="alert alert-danger"> {{ errorMessage }} </div>

            <div v-else-if="trek" class="card shadow-sm">
                <div class="card-header">
                    <h5 class="card-title">Trek Details</h5>
                </div>

                <div class="card-body">
                    <div class="mb-4">
                        <h5>{{ trek.trek_name }}</h5>
                        <p class="text-muted mb-1">Location: {{ trek.location }}</p>
                        <p class="text-muted mb-1">Duration: {{ trek.duration }} day(s)</p>
                        <p class="text-muted mb-0">Current Status: <strong>{{ trek.status }}</strong></p>
                    </div>

                    <div v-if="errorMessage" class="alert alert-danger">
                        {{ errorMessage }}
                    </div>

                    <form @submit.prevent="scheduleTrek">
                        <div class="mb-3">
                            <label for="start_date" class="form-label">Start Date:</label>
                            <input id="start_date" v-model="scheduleForm.start_date" type="date" class="form-control" :min="today" required>
                        </div>

                        <div class="mb-3">
                            <label for="end_date" class="form-label">End Date (Auto Calculated)</label>
                            <input id="end_date" :value="formatDate(calculatedEndDate)" type="type" class="form-control" placeholder="Select a start date first" readonly>
                        </div>

                        <div class="mb-4">
                            <label for="total_slot" class="form-label">Total Slots:</label>
                            <input id="total_slot" v-model.number="scheduleForm.total_slot" class="form-control" type="number" min="1" step="1" required>
                        </div>

                        <button type="submit" class="btn btn-success" :disabled="submitting || !calculatedEndDate">
                            {{ submitting ? 'Scheduling...' : 'Confirm Schedule' }}
                        </button>

                        <RouterLink to="/admin_dashboard/treks" class="btn btn-secondary ms-2">
                            Cancel
                        </RouterLink>
                    </form>
                </div>
            </div>

        </main>
    </div>
</template>




<script setup>

import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import DashNavbar  from '@/components/DashNavbar.vue';
import AdminSidebar from '@/components/AdminSidebar.vue';


const route = useRoute();
const router = useRouter();

const trek = ref(null);
const loading = ref(false);
const errorMessage = ref('');
const submitting = ref(false);

const scheduleForm = ref({
    start_date: '',
    total_slot: 20
})

const trekId = route.params.trek_id;

function getLocalDateString(date = new Date()) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

const today = getLocalDateString();

const calculatedEndDate = computed(() => {
    if (!scheduleForm.value.start_date || !trek.value) return '';

    const duration = Number(trek.value.duration);

    if (!Number.isInteger(duration) || duration < 1) return '';

    const startDate = new Date(`${scheduleForm.value.start_date}T00:00:00`);

    startDate.setDate(startDate.getDate() + duration - 1);
    
    return getLocalDateString(startDate);
});

function formatDate(dateString) {
    if (!dateString) return '';

    const [year, month, day] = dateString.split('-');
    return `${day}/${month}/${year}`;
}

async function getTrek() {
    loading.value = true;
    errorMessage.value = '';

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/admin_dashboard/treks`, {
            headers: {
                'Authentication-Token': localStorage.getItem('auth_token')
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to load trek.');
        }

        trek.value = data.find(item => String(item.trek_id) === String(trekId));

        if (!trek.value) {
            throw new Error('Trek not found.');
        }
    } catch (error) {
        errorMessage.value = error.message;
    } finally {
        loading.value = false;
    }
}

async function scheduleTrek() {
    errorMessage.value = '';

    if (!trek.value) return;

    if (!scheduleForm.value.start_date) {
        errorMessage.value = 'Please select a start date.';
        return;
    }

    if (!scheduleForm.value.start_date < today) {
        errorMessage.value = 'Start date cannot be in the past.';
        return;
    }

    const totalSlot = Number(scheduleForm.value.total_slot);

    if (!Number.isInteger(totalSlot) || totalSlot < 1) {
        errorMessage.value = 'Total slots must be at least 1.';
        return;
    }

    submitting.value = true;

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/admin_dashboard/treks/${trekId}/schedule`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth_token')
            },
            body: JSON.stringify({
                start_date: scheduleForm.value.start_date,
                total_slot: totalSlot
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || 'Failed to schedule trek.');
        }

        alert(
            `${result.message}\n` +
            `Start: ${formatDate(result.start_date)}\n` +
            `End: ${formatDate(result.end_date)}`
        );

        await router.push('/admin_dashboard/treks');
    } catch (error) {
        errorMessage.value = error.message;
    } finally {
        submitting.value = false;
    }
}

onMounted(() => {
    getTrek();
});



</script>