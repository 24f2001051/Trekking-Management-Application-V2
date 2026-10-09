

<template>

    <DashNavbar />
    <div class="d-flex">
        <AdminSidebar />
        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Staff</h1>

                <RouterLink
                    to="/admin_dashboard/staff/add_staff"
                    class="btn btn-success"
                >
                    + Add New Staff
                </RouterLink>
            </div>
            <div class="input-group mb-4">
                <input
                    type="text"
                    class="form-control"
                    placeholder="Search staff..."
                    v-model="search"
                >
                <button class="btn btn-outline-secondary"> 🔍 </button>
            </div>

            <table class="table table-bordered table-hover align-middle">
                <thead class="table-light">
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col">Staff Name</th>
                        <th scope="col">Username</th>
                        <th scope="col">Designation</th>
                        <th scope="col">Assigned Trek</th>
                        <th scope="col">Status</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="staff in filteredStaffs" :key="staff.staff_id">
                        <td>{{ staff.staff_id }}</td>
                        <td>{{ staff.fullname }}</td>
                        <td>{{ staff.username }}</td>
                        <td>{{ staff.designation }}</td>
                        <td>
                            <select
                                class="form-select"
                                :value="staff.assigned_trek_id ?? ''"
                                @change="assignTrek(staff.staff_id, $event.target.value)"
                            >
                                <option value="">Not Assigned</option>

                                <option
                                    v-for="trek in availableTreks(staff)"
                                    :key="trek.trek_id"
                                    :value="trek.trek_id"
                                >
                                    {{ trek.trek_name }}
                                </option>
                            </select>
                        </td>
                        <td>
                            <span
                                class="badge"
                                :class="staff.status ? 'bg-success' :  'bg-danger'"
                            >
                                {{
                                    staff.status
                                    ? 'Active'
                                    : 'Inactive'
                                }}
                            </span>
                        </td>

                        <td>
                            <RouterLink
                                :to="`/admin_dashboard/staff/edit_staff/${staff.staff_id}`"
                                class="btn btn-primary"
                            >
                                Edit
                            </RouterLink>
                            <button
                                class="btn btn-sm btn-danger"
                                @click="deleteStaff(staff)"
                            >
                                🗑️
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </main>
    </div>


</template>


<script setup>

import { ref, computed, onMounted } from "vue"

import DashNavbar from '../components/DashNavbar.vue'
import AdminSidebar from '../components/AdminSidebar.vue'

const search = ref("")
const staffs = ref([])
const treks = ref([])

async function getStaffs(){
    const response = await fetch(
        "http://localhost:5000/api/admin_dashboard/staff",
        {
            headers: {
                "Authentication-Token": localStorage.getItem("auth_token")
            }
        }
    )
    if (!response.ok) {
        console.error(
            "Staff API error:",
            response.status
        )
        return
    }
    staffs.value = await response.json()
    console.log("Staff data:", staffs.value)
}


function availableTreks(staff) {
    return treks.value.filter(trek =>
        !trek.assign_staff_id ||
        String(trek.assign_staff_id) === String(staff.id)
    )
}

async function getTreks() {
    const response = await fetch(
        'http://127.0.0.1:5000/api/admin_dashboard/treks',
        {
            headers: {
                'Authentication-Token': localStorage.getItem('auth_token')
            }
        }
    )

    if (!response.ok) {
        throw new Error('Failed to fetch treks')
    }

    treks.value = await response.json()
}

async function assignTrek(staffId, selectedTrekId) {
    try {
        const response = await fetch(
            `http://127.0.0.1:5000/api/admin_dashboard/staff/${staffId}/assigned_trek`,
            {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                    trek_id: selectedTrekId === ''
                        ? null
                        : Number(selectedTrekId)
                })
            }
        )

        const result = await response.json()

        if (!response.ok) {
            alert(result.message || 'Failed to update trek assignment')
            await getStaffs()
            await getTreks()
            return
        }

        alert(result.message)
        await getStaffs()
        await getTreks()

    } catch (error) {
        console.error('Error assigning trek:', error)
        alert('Could not update trek assignment. Check the backend console.')
    }
}



async function deleteStaff(staff) {
    if (!confirm(`Permanently delete ${staff.fullname}?`)) return

    try {
        const response = await fetch(
            `http://127.0.0.1:5000/api/admin_dashboard/users/${staff.staff_id}`,
            {
                method: "DELETE",
                headers: {
                    "Authentication-Token": localStorage.getItem("auth_token")
                }
            }
        )

        const data = await response.json()

        if (!response.ok) {
            alert(data.message || "Could not delete staff")
            return
        }

        alert("Staff deleted successfully")
        await getStaffs()
    } catch (error) {
        console.error(error)
        alert("Could not connect to the server")
    }
}



const filteredStaffs = computed(() => {
    const text = search.value.trim().toLowerCase()

    return staffs.value.filter(staff => {
        const status = staff.status ? 'active' : 'inactive'

        const matchesStatus = status.includes(text) &&
        (
            !['active', 'inactive'].includes(text) ||
            status === text
        )
        const assignedTreks = Array.isArray(staff.assigned_treks)
            ? staff.assigned_treks.join(', ').toLowerCase()
            : ''

        return (
            String(staff.fullname ?? '').toLowerCase().includes(text) ||
            String(staff.username ?? '').toLowerCase().includes(text) ||
            String(staff.designation ?? '').toLowerCase().includes(text) ||
            assignedTreks.includes(text) ||
            matchesStatus
        )
    })
})



async function changeStatus(id, active){
    const response = await fetch(
        "http://localhost:5000/api/admin_dashboard/staff/${id}/status",
        {
            method: "PUT",
            body: JSON.stringify({
                active: active
            }),
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": localStorage.getItem("auth_token")
            }
        }
    )
    if (!response.ok) {
        const data = await response.json()
        alert(data.message)
        return
    }
    getStaffs()
}

onMounted(async () => {
    await getStaffs()
    await getTreks()

})


</script>