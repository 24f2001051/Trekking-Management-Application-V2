<template>
    <DashNavbar />
    <div class="d-flex">
        <StaffSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Participants</h2>

                <button class="btn btn-outline-primary" @click="getParticipants" :disabled="loading"> Refresh </button>
            </div>

            <div v-if="errorMessage" class="alert alert-danger"> {{ errorMessage }} </div>
            
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        Participants of {{ trekName || 'Assigned Trek' }}
                    </h4>
                </div>

                <div class="card-body p-4">



                    <div v-if="loading" class="text-center p-4">Loading participants...</div>

                    <div v-else class="table-responsive">
                        <table class="table table-bordered table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Booking ID</th>
                                    <th>TrekkerName</th>
                                    <th>Username</th>
                                    <th>Email</th>
                                    <th>Phone</th>
                                    <th>Booking Date</th>
                                    <th>Booking Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="participant in filteredParticipants" :key="participant.booking_id">
                                    <td>{{ participant.booking_id }}</td>
                                    <td>{{ participant.fullname }}</td>
                                    <td>{{ participant.username }}</td>
                                    <td>{{ participant.email }}</td>
                                    <td>{{ participant.phone || 'N/A' }}</td>

                                    <td>{{ participant.booking_date || 'N/A' }}</td>
                                    <td>
                                        <span
                                            class="badge"
                                            :class="participant.booking_status === 'Cancelled'
                                                ? 'bg-danger'
                                                : 'bg-success'"
                                        >                                        
                                            {{ participant.booking_status }}
                                        </span>
                                    </td>
                                </tr>

                                <tr v-if="filteredParticipants.length === 0">
                                    <td colspan="7" class="text-center" >No participants found.</td>
                                </tr>





                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </main>
    </div>

</template>


<script setup>
import { ref, onMounted, computed } from "vue";
import DashNavbar from '@/components/DashNavbar.vue';
import StaffSidebar from '@/components/StaffSidebar.vue';

const API = 'http://127.0.0.1:5000/api';

const loading = ref(false);
const errorMessage = ref('');
const trekName = ref('');
const participants = ref([]);
const searchQuery = ref('');

const filteredParticipants = computed(() => {
    const query = searchQuery.value.trim().toLowerCase();

    if (!query) {
        return participants.value;
    }

    return participants.value.filter(participant => {
        return [
            participant.booking_id,
            participant.fullname,
            participant.username,
            participant.email,
            participant.phone,
            participant.booking_date,
            participant.status
        ].some(value => String(value || '').toLowerCase().includes(query) )
    });
});

async function getParticipants() {
    loading.value = true;
    errorMessage.value = '';

    try {
        const token = localStorage.getItem('auth_token');

        if (!token) {
            throw new Error('Please log in again.');
        }

        const response = await fetch(`${API}/staff_dashboard/participants`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Unable to load participants.');
        }

        trekName.value = data.trek || '';
        participants.value = data.participants || [];
    } catch (error) {
        errorMessage.value = error.message || 'An error occurred.';
    } finally {
        loading.value = false;
    }
}

onMounted(getParticipants);

</script>