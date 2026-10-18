<template>
    <DashNavbar />
    <div class="d-flex">
        <AdminSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Edit Trek</h1>
            </div>
            <form v-on:submit.prevent="editTrek">
                <div class="mb-3">
                    <label for="InputTrekName" class="form-label">Trek Name:</label>
                    <input type="text" class="form-control" id="InputTrekName" placeholder="input trek name here"  v-model="trek.trek_name" required>
                </div>
                <div class="mb-3">
                    <label for="InputLocation" class="form-label">Location:</label>
                    <input type="text" class="form-control" id="InputLocation" placeholder="input location here" required v-model="trek.location">
                </div>
                <div class="mb-3">
                    <label for="InputDifficulty" class="form-label">Difficulty:</label>
                    <select class="form-select" id="InputDifficulty" placeholder="input difficulty here" required v-model="trek.difficulty">
                        <option value="Explorer">Explorer(Beginner)</option>
                        <option value="Adventurer">Adventurer(Intermediate)</option>
                        <option value="Trailblazer">Trailblazer(Advanced)</option>
                    </select>
                </div>

                <div class="mb-3">
                    <label for="InputDuration" class="form-label">Duration (in days):</label>
                    <input type="number" class="form-control" min="1" id="InputDuration" placeholder="input duration here" required v-model="trek.duration">
                </div>

                <div class="mb-3">
                    <label for="InputDescription" class="form-label">Description:</label>
                    <textarea class="form-control" id="InputDescription" placeholder="input description here" required v-model="trek.description"></textarea>
                </div>

                <div class="mb-3">
                    <label for="AssignTrekStaff" class="form-label">Assign Trek Staff:</label>
                    <select class="form-select" id="AssignTrekStaff" placeholder="input trek staff here" required v-model="trek.assign_staff_id">
                        <option :value="null">No Staff Assigned</option>
                        <option v-for="staff in staffs" :key="staff.staff_id" :value="staff.staff_id">
                            {{ staff.fullname }}
                        </option>
                    </select>
                </div>

                <div class="mb-4">
                    <label class="form-label">Status: </label>
                    <select class="form-select" id="InputStatus" required v-model="trek.status">
                        <option value="Active">Active</option>
                        <option value="Inactive">Inactive</option>
                    </select>
                </div>


                <div class="text">
                    <button type="button" class="btn btn-primary fw-bold" @click="router.push('/admin_dashboard/treks')">Back</button>
                    <input type="submit" class="btn btn-success" value="Update Trek">
                </div>
            </form>
        </main>
    </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import { useRoute, useRouter } from 'vue-router';

import DashNavbar from '@/components/DashNavbar.vue';
import AdminSidebar from '@/components/AdminSidebar.vue';

const route = useRoute();
const router = useRouter();

const staffs = ref([]);

const trek = ref({
    trek_name: "",
    location: "",
    difficulty: "",
    duration: "",
    description: "",
    assign_staff_id: null,
    status: "Inactive"
});

async function getTrek() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/admin_dashboard/treks`,
            {
                headers: {
                    "Authentication-Token": localStorage.getItem("auth_token")
                }
            }
        )

        if (!response.ok) {
            throw new Error('Failed to fetch treks')
        }

        const data = await response.json()

        const found = data.find(item =>item.trek_id == route.params.id)

        if (found) {
            trek.value = {
                trek_name: found.trek_name ?? '',
                location: found.location ?? '',
                difficulty: found.difficulty ?? '',
                duration: found.duration ?? '',
                description: found.description ?? '',
                assign_staff_id: found.assigned_staff_id ?? null,
                status: found.status ?? 'Inactive'
            
            }
        } else {
            alert('Trek not found')
            router.push('/admin_dashboard/treks')
        }

        console.log("Trek data: ", found)
        console.log("Assigned staff ID: ", found.assigned_staff_id)

    } catch (error) {
        console.error('Error fetching treks:', error)
        alert('Unable to load trek details')
    }    
}

async function getStaffs() {
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/admin_dashboard/staff_options",
            {
                headers: {
                    "Authentication-Token": localStorage.getItem("auth_token")
                }
            }
        )
        if (!response.ok) {
            throw new Error('Failed to fetch staff')
        }

        staffs.value = await response.json()
        console.log("Staff options: ", staffs.value)

    } catch (error) {
        console.error('Error fetching staff:', error)
        alert('Unable to load staff options')
    }
}

async function editTrek() {
    try {
        const response = await fetch(
            `http://127.0.0.1:5000/api/admin_dashboard/treks/${route.params.id}/edit`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": localStorage.getItem("auth_token")
                },
                body: JSON.stringify(trek.value)
            }
        )
        const data = await response.json();
        console.log(data);

        if (!response.ok) {
            alert(data.message || "Unable to update trek");
            return
        }
        alert(data.message ||"Trek updated successfully");
        router.push("/admin_dashboard/treks")

    } catch (error) {
        console.error("Error updating trek:", error);
        alert("Unable to connect to the server");
    }
}

onMounted(() => {
    getTrek();
    getStaffs();
});


</script>