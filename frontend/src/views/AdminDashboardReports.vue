<template>

    <DashNavbar />

    <div class="d-flex">
        <AdminSidebar />
        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Reports & Statistics</h1>

                <div class="row g-3">
                    <div class="col-md-3">
                        <div class="card p-3">
                            <h6>Total Treks</h6>
                            <h2>{{ reports.total_treks }}</h2>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card p-3">
                            <h6>Active Treks</h6>
                            <h2>{{ reports.active_treks }}</h2>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card p-3">
                            <h6>Inactive Treks</h6>
                            <h2>{{ reports.inactive_treks }}</h2>
                        </div>
                    </div>

                    <div class="col-md-3">
                        <div class="card p-3">
                            <h6>Total Users</h6>
                            <h2>{{ reports.total_users }}</h2>
                        </div>
                    </div>

                    <div class="col-md-3">
                        <div class="card p-3">
                            <h6>Total Staff</h6>
                            <h2>{{ reports.total_staff }}</h2>
                        </div>
                    </div>

                    <div class="col-md-3">
                        <div class="card p-3">
                            <h6>Total Bookings</h6>
                            <h2>{{ reports.total_bookings }}</h2>
                        </div>
                    </div>

                    <div class="col-md-3">
                        <div class="card p-3">
                            <h6>Booked</h6>
                            <h2>{{ reports.confirmed_bookings }}</h2>
                        </div>
                    </div>

                    <div class="col-md-3">
                        <div class="card p-3">
                            <h6>Cancelled</h6>
                            <h2>{{ reports.cancelled_bookings }}</h2>
                        </div>
                    </div>

                </div>
            </div>
        </main>
    </div>

</template>



<script setup>
import { ref, onMounted } from "vue";

import DashNavbar from '../components/DashNavbar.vue'
import AdminSidebar from '../components/AdminSidebar.vue'

const reports = ref({
    total_treks: 0,
    active_treks: 0,
    total_users: 0,
    total_staff: 0,
    total_bookings: 0,
    confirmed_bookings: 0,
    cancelled_bookings: 0
})
async function getReports() {

    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/admin_dashboard/reports",
            {
                headers: {
                    "Authentication-Token": localStorage.getItem("auth_token")
                }
            }
        )
        if (!response.ok) {
            console.error("Reports API error:", response.status)
            throw new Error(`HTTP ${response.status}`)
        }
        const data = await response.json()

        reports.value = {
            ...reports.value,
            ...data
        }

    } catch (error) {
        console.error("Reports API error:", error)
    }
}

onMounted(() => {
    getReports()
})


</script>