<template>
    <DashNavbar />

    <div class="d-flex">
        <StaffSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>My Profile</h2>

                <button class="btn btn-outline-primary" @click="getProfile" :disabled="loading"> Refresh </button>
            </div>

            <div v-if="errorMessage" class="alert alert-danger"> {{ errorMessage }} </div>

            <div v-if="loading" class="text-center p-4"> Loading profile... </div>
            
            <div v-else class="card shadow-sm mb-4">
                <div class="card-header bg-primary bg-white">
                    <h4 class="mb-0">Staff ID: {{ profile.staff_id ?? 'N/A'}} 's Info</h4>
                </div>

                <div class="card-body p-4">

                    <!-- <div class="trek-detail">
                        <span class="detail-label">Staff ID: </span>
                        <span> {{ profile.staff_id ?? 'N/A' }}</span>
                    </div> -->

                    <div class="trek-detail">
                        <span class="detail-label">Full Name: </span>
                        <span> {{ profile.fullname || 'N/A' }}</span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Username: </span>
                        <span> {{ profile.username || 'N/A' }}</span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Email: </span>
                        <span> {{ profile.email || 'N/A' }}</span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Phone no.: </span>
                        <span> {{ profile.phone || 'Not provided' }}</span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Designation: </span>
                        <span> {{ profile.designation || 'Not provided' }}</span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Experience: </span>
                        <span> {{
                                profile.experience_years != null
                                    ? `${profile.experience_years} years`
                                    : 'Not provided'
                            }}
                        </span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Assigned Trek: </span>
                        <span> {{ profile.assigned_trek || 'N/A' }}</span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Address: </span>
                        <span> {{ profile.address || 'No provided.' }} </span>
                    </div>

                    
                    
                </div>
            </div>

        </main>
    </div>

</template>





<script setup>

import { ref, onMounted } from 'vue';
import DashNavbar from '@/components/DashNavbar.vue';
import StaffSidebar from '@/components/StaffSidebar.vue';

const API = 'http://127.0.0.1:5000/api';

const loading = ref(false);
const errorMessage = ref('');
const profile = ref({});

async function getProfile() {
    loading.value = true;
    errorMessage.value = '';

    try {
        const token = localStorage.getItem('auth_token');

        if (!token) {
            throw new Error('Please log in again.');
        }

        const response = await fetch(`${API}/staff_dashboard/profile`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Unable to load profile.');
        }
        profile.value = data


    } catch (error) {
        errorMessage.value = error.message || 'An error occurred.';
    } finally {
        loading.value = false;
    }
}

onMounted(() => {
    getProfile();
});




</script>


<style scoped>

.card {
    border-radius: 10px;
    overflow: hidden;
}

.card-header h4 {
    font-size: 28px;
    font-weight: 600;
}

.card-body {
    padding: 28px !important;
    background-color: rgb(135 206 250 / 20%);

}

.trek-detail {
    display: flex;
    align-items: baseline;
    gap: 18px;    
    margin-bottom: 20px;
    font-size: 19px;
    line-height: 1.6;
    font-weight: 500;
}

.detail-label {
    font-weight: 650;
    min-width: 125px;
    flex-shrink: 0;
}

.description {
    overflow-wrap: anywhere;
}

</style>