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
                        <option value="null">No Staff Assign</option>
                        <option v-for="staff in staffs" :key="staff.id" :value="staff.id">
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

<script>
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
    const response = await fetch(`http://127.0.0.1:5000/api/treks`)
    const data = await response.json()

    const found = data.first(item =>item.trek_id == route.params.id)

    if (found) {
        trek.value = {
            ...found,
            description: "",
            assign_staff_id: null
        }
    }
}

async function getStaffs() {
    const response = await fetch(
        "http://127.0.0.1:5000/api/admin_dashboard/staff_options",
        {
            headers: {
                "Authentication-Token": localStorage.getItem("auth_token")
            }
        }
    ) 
    staffs.value = await response.json()
}

async function updateTreks() {
    const response = await fetch(
        `http://127.0.0.1:5000/api/admin_dashboard/treks/${route.params.trek_id}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": localStorage.getItem("auth_token")
            },
            body: JSON.stringify(trek.value)
        }
    ) 
    if (!response.ok) {
        const errorData = await response.json();
        console.error(errorData);
        alert(`Updating a Trek failed: ${errorData.message}`);
        return
    }
    alert("Trek updated successfully");
    router.push("/admin_dashboard/treks")
}

onMounted(() => {
    getTrek();
    getStaffs();
});


</script>