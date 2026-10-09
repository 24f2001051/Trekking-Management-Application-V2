<template>
    <div class="sidebar bg-light border-end vh-100">
    
        <ul class="nav flex-column p-3">
    
            <li class="nav-item mb-2">
                <RouterLink class="nav-link" to="/admin_dashboard">
                    🏠 Dashboard
                </RouterLink>
            </li>
    
            <li class="nav-item mb-2">
                <RouterLink class="nav-link" to="/admin_dashboard/treks">
                    🥾 Treks
                </RouterLink>
            </li>
    
            <li class="nav-item mb-2">
                <RouterLink class="nav-link" to="/admin_dashboard/staff">
                    👨‍💼 Trekking Staff
                </RouterLink>
            </li>
    
            <li class="nav-item mb-2">
                <RouterLink class="nav-link" to="/admin_dashboard/users">
                    👥 Users
                </RouterLink>
            </li>
    
            <li class="nav-item mb-2">
                <RouterLink class="nav-link" to="/admin_dashboard/bookings">
                    📅 Bookings
                </RouterLink>
            </li>
            
    
            <li class="nav-item mb-2">
                <RouterLink class="nav-link" to="/admin_dashboard/reports">
                    📊 Reports
                </RouterLink>
            </li>
    
    
            <li class="nav-item mt-4">
                <button class="btn btn-outline-danger w-100" @click="logout">
                    Logout
                </button>
            </li>
    
        </ul>
    
    </div>
    
</template>
    
<style scoped>
    .sidebar{
        width:240px;
        min-height:100vh;
    }
    
    .nav-link{
        color:#333;
        font-weight:500;
    }
    
    .nav-link:hover{
        background:#e9ecef;
        border-radius:8px;
    }
    
    .router-link-active{
        background:#dbeafe;
        color:#0d6efd !important;
        border-radius:8px;
        font-weight:600;
    }
</style>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useRouter } from 'vue-router'; // 1. Import it
const router = useRouter(); // 2. Define it
const fullname = localStorage.getItem('fullname');

async function logout() {

    try {

        const token = localStorage.getItem("auth_token");
        const response = await fetch("http://127.0.0.1:5000/api/logout",
        {
            method: "POST",
            headers: {
                "Authentication-Token": token
            }
        });
        if (!response.ok) {
            console.error("Logout API error:", response.status, await response.text());
        }
    } catch (error) {
        console.error("Logout API error:", error);
    } finally {
        localStorage.clear();
        console.log("Logout successful");
        router.push("/login");
    }
}
</script>
