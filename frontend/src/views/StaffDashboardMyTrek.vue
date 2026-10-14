<template>
    <DashNavbar />

    <div class="d-flex">
        <StaffSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>My Assigned Trek</h2>
                <button class="btn btn-outline-primary" @click="getTreks" :disabled="loading"> Refresh </button>
            </div>

            <div v-if="errorMessage" class="alert alert-danger"> {{ errorMessage }} </div>
            <div v-else-if="loading" class="text-center p-4"> Loading assigned trek... </div>

           
            <div v-else-if="trek" class="card shadow-sm mb-4">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0"> {{ trek.trek_name }} </h4>
                </div>

                <div class="card-body p-4">
                    <div class="trek-detail">
                        <span class="detail-label">Location: </span>
                        <span> {{ trek.location }}</span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Difficulty: </span>
                        <span> {{ trek.difficulty }}</span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Duration: </span>
                        <span> {{ trek.duration }} days</span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Trek Status: </span>
                        <span> <span
                                class="badge"
                                :class="trek.status === 'Active'
                                    ? 'bg-success'
                                    : 'bg-danger'"
                            > {{ trek.status }} </span>
                        </span>
                    </div>

                    <div class="trek-detail">
                        <span class="detail-label">Description: </span>
                        <span  class="description"> {{ trek.description || 'No description available.' }} </span>
                    </div>
                </div>
            </div>
            <div v-else class="alert alert-info">
                No trek is currently assigned to you.
            </div>
        </main>
    </div>

</template>

<script setup>
import DashNavbar from '@/components/DashNavbar.vue';
import StaffSidebar from '@/components/StaffSidebar.vue';

import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const trek = ref(null);
const loading = ref(false);
const errorMessage = ref('');

const router = useRouter();
const API = 'http://127.0.0.1:5000/api';

async function getTrek() {
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
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': token
                }
            }
        );
        const data = await response.json();

        if (!response.ok) {
            if (response.status === 404) {
                trek.value = null;
                return
            }
            throw new Error(data.message || 'Failed to fetch assigned trek details.');        
        }
        trek.value = data.trek || null;
    } catch (error) {
        errorMessage.value = error.message;
    } finally {
        loading.value = false;
    }
}

onMounted(() => {
    getTrek();
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
    gap: 10px;    
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