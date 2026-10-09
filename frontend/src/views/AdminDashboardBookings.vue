<template>
    <DashNavbar />
    <div class="d-flex">
        <AdminSidebar />
        <main class="flex-grow-1 p-4">
            <h1 class="mb-4">Bookings</h1>
            <input type="text" class="form-control mb-4" placeholder="Search bookings..." v-model="search">
            <table class="table table-bordered table-hover">
                <thead class="table-light">
                    <tr>
                        <th>Booking ID</th>
                        <th>User</th>
                        <th>Trek</th>
                        <th>Booking Date</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="booking in filteredBookings" :key="booking.booking_id">
                        <td>{{ booking.booking_id }}</td>
                        <td>{{ booking.user }}</td>
                        <td>{{ booking.trek }}</td>
                        <td>{{ booking.booking_date }}</td>
                        <td>
                            <span class="badge bg-success">
                                {{ booking.status }}
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </main>
    </div>


</template>

<script setup>

import { ref, onMounted ,computed } from 'vue';

import AdminSidebar from '@/components/AdminSidebar.vue';
import DashNavbar from '@/components/DashNavbar.vue';

const bookings = ref([])
const search = ref("")

async function getBookings() {
    try {
        const response = await fetch(
            "http://localhost:5000/api/admin_dashboard/bookings",
            {
                headers: {
                    "Authentication-Token": localStorage.getItem("auth_token")
                }
            }
        )
        if (!response.ok) {
            console.error( "Bookings API error:", response.status )
            throw new Error(`HTTP ${response.status}`)
        }
        const data = await response.json()

        bookings.value = Array.isArray(data)
            ? data.map(booking => ({ ...booking, booking_date: booking.booking_date ?? booking.booking_date ?? "" })) : []
    } catch (error) {
        console.error("Bookings API error:", error)
        bookings.value = []
    }
}

const filteredBookings = computed(() => {
    const text = search.value.trim().toLowerCase()

    return bookings.value.filter(booking =>
        String(booking.user ?? "").toLowerCase().includes(text) ||
        String(booking.trek ?? "").toLowerCase().includes(text) ||
        String(booking.booking_date ?? "").toLowerCase().includes(text) ||
        String(booking.status ?? "").toLowerCase().includes(text)
)
})

onMounted(() => {
    getBookings()
})






</script>