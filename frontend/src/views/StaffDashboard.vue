<template>
    <DashNavbar />
    
    <div class="d-flex">
        <StaffSidebar />
    
        <main class="flex-grow-1 p-4">
            <h1>STAFF DASHBOARD</h1>
            <br>

            <!-- OR your dashboard cards -->

        <div class="row g-3 mb-4">

            <div class="col-md-3">
                <div class="card-body">
                    <h6>Assigned Treks</h6>
                    <h2>{{ dashboard.assigned_trek }}</h2>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card-body">
                    <h6>Total Participants</h6>
                    <h2>{{ dashboard.total_participants }}</h2>
                </div>
            </div>
    
            <div class="col-md-3">
                <div class="card-body">
                    <h6>Upcoming Treks</h6>
                    <h2>{{ dashboard.upcoming_trek_count }}</h2>
                </div>
            </div>


        </div>
        <br>
        <div class="card mt-4 shadow-sm">   <!-- upcoming trek card -->
            <div class="card-header bg-white">
                <h5 class="mb-0">Upcoming Trek booking</h5>
            </div>

            <div class="card-body">
                <div v-if="loading" class="text-center p-3"> Loading upcoming schedules... </div>

                <div v-else-if="errorMessage" class="alert alert-danger"> {{ errorMessage }} </div>

                <div v-else class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>Trek Name</th>
                                <th>Dates</th>
                                <th>Participants</th>
                                <th>Slots</th>
                                <th>Status</th>
                                <th>Active</th>
                            </tr>
                        </thead>
        
                        <tbody>
                            <tr
                                v-for="trek in dashboard.overall_treks"
                                :key="trek.availability_id ?? 'Trek-${trek.trek_id}'"
                            >
                                <td>{{ trek.trek_name }}</td>
                                <td>
                                    {{
                                        trek.start_date === trek.end_date
                                            ? $formatDate(trek.start_date)
                                            : `${$formatDate(trek.start_date)} - ${$formatDate(trek.end_date)}`
                                    }}

                                </td>
                                <td>{{ trek.participants }}</td>
                                <td>{{ trek.avail_slot }}</td>
                                <td>
                                    <span
                                        class="badge"
                                        :class="{
                                            'text-bg-success': trek.status == 'Open',
                                            'text-bg-danger': trek.status == 'Closed',
                                            'text-bg-secondary': trek.status == 'Not Scheduled',
                                        }"
                                    >
                                        {{ trek.status }}</span>
                                </td>

                                <td>
                                    <button
                                        class="btn btn-outline-primary btn-sm"
                                        @click="manageTrek(trek)"
                                    >
                                        {{ trek.status == 'Closed' ? 'View' : 'Manage'}}
                                    </button>
                                </td>
                            </tr>
                            <tr v-if="dashboard.overall_treks.length === 0">
                                <td colspan="6" class="text-center">No upcoming trek schedules available.</td>
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
import { ref, onMounted } from "vue";
import DashNavbar from '../components/DashNavbar.vue'
import StaffSidebar from '@/components/StaffSidebar.vue';
import { useRouter } from 'vue-router'; // 1. Import it
const router = useRouter(); // 2. Define it

const fullname = localStorage.getItem('fullname') || 'Staff';

const dashboard = ref({
    assigned_trek: null,
    total_participants: 0,
    overall_treks: [],
    upcoming_treks: [],
    upcoming_treks_count: 0,
})

const loading = ref(false);
const errorMessage = ref('');


async function getDashboard() {

    loading.value = true;
    errorMessage.value = '';

    try {
        
        const response = await fetch("http://127.0.0.1:5000/api/staff_dashboard", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": localStorage.getItem("auth_token")
            }
        });

        if (!response.ok) {
            throw new Error(`Unable to load dashboard: HTTP ${response.status}`);
        }

        dashboard.value = await response.json();

    } catch (err) {
        console.error('Staff Dashboard error:', err);
        errorMessage.value = err.message || 'Unable to load dashboard';
    } finally {
        loading.value = false;
    }
}

function manageTrek(trek) {
    router.push({
        path: '/staff_dashboard/manage_trek',
        query: {
            trek_id: trek.trek_id,
            availability_id: trek.availability_id
        }
    });
}

onMounted(() => {
    getDashboard();
});

</script>