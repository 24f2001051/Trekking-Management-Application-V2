<template>
<DashNavbar />

<div class="d-flex">
    <AdminSidebar />

    <main class="flex-grow-1 p-4">
        <h1>{{ role.toUpperCase () }} DASHBOARD</h1>
        <br>
        <!-- OR your dashboard cards -->
    
    <div class="row g-3">
        <div class="col-md-3">
            <div class="card-body">
                <h6>Total Treks</h6>
                <h2>{{ dashboard.total_treks }}</h2>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card-body">
                <h6>Total Users</h6>
                <h2>{{ dashboard.total_users }}</h2>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card-body">
                <h6>Total Trekking Staff</h6>
                <h2>{{ dashboard.total_staff }}</h2>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card-body">
                <h6>Total Bookings</h6>
                <h2>{{ dashboard.total_bookings }}</h2>
            </div>
        </div>
    </div>
    <br>
    <div class="card mt-4 shadow-sm">   <!-- Booking card -->
        <div class="card-header">
            <h5 class="mb-0">Recent Bookings</h5>
        </div>
        <div class="card-body">
            <table class="table table-hover">
                <thead> <tr>
                        <th>Booking ID</th>
                        <th>User</th>
                        <th>Trek</th>
                        <th>Booking Date</th>
                        <th>Status</th>
                </tr> </thead>

                <tbody>
                    <tr
                        v-for="booking in dashboard.recent_bookings"
                        :key="booking.booking_id"
                    >
                        <td>{{ booking.booking_id }}</td>
                        <td>{{ booking.user }}</td>
                        <td>{{ booking.trek }}</td>
                        <td>{{ booking.booking_date }}</td>
                        <td>{{ booking.status }}</td>
                    </tr>
                </tbody>

            </table>
            <div class="text-end">
                <RouterLink
                    to="/admin_dashboard/bookings"
                    class="text-decoration-none fw-bold"
                >
                    View All Bookings →
                </RouterLink>

            </div>

        </div>

    </div>




    </main>




</div>   
</template>

<script setup>
import { ref, onMounted } from "vue";
import DashNavbar from '../components/DashNavbar.vue'
import AdminSidebar from '@/components/AdminSidebar.vue';
import { useRouter } from 'vue-router'; // 1. Import it
const router = useRouter(); // 2. Define it

const role = localStorage.getItem('role');
const id = localStorage.getItem('id');
const username = localStorage.getItem('username');
const fullname = localStorage.getItem('fullname');
const email = localStorage.getItem('email');

const dashboard = ref({
    total_treks: 0,
    total_users: 0,
    total_staff: 0,
    total_bookings: 0,
    recent_bookings: []
})

async function getDashboard() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/admin_dashboard", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": localStorage.getItem("auth_token")
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        dashboard.value = data;

    } catch (err) {
        console.error(err);
    }
}
onMounted(() => {
    getDashboard();
});

</script>