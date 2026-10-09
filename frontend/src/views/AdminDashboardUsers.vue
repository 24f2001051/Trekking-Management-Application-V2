<template>
    <DashNavbar />
    <div class="d-flex">
        <AdminSidebar />
        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Users (Trekkers)</h1>
            </div>
            <input type="text" class="form-control mb-4" placeholder="Search users..." v-model="search">

            <table class="table table-bordered table-hover">
                <thead> <tr>
                        <th>ID</th>
                        <th>Full Name</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="user in filteredUsers"
                        :key="user.user_id"
                    >
                        <td>{{ user.user_id }}</td>
                        <td>{{ user.fullname }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.email }}</td>
                        <td>
                            <span
                                class="badge"
                                :class="
                                    user.status=='Active'
                                    ? 'bg-success'
                                    : 'bg-danger'"
                            >
                                {{
                                    user.status
                                    ? 'Active'
                                    : 'Inactive'
                                }}
                            </span>
                        </td>

                        <td>
                            <button
                                class="btn btn-sm btn-danger"
                                @click="deleteUser(user)"
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
import {ref , onMounted, computed} from 'vue'

import DashNavbar from '../components/DashNavbar.vue'
import AdminSidebar from '../components/AdminSidebar.vue'

const users = ref([])
const search = ref('')

async function getUsers() {
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/admin_dashboard/users",
            {
                headers: {
                    "Authentication-Token": localStorage.getItem("auth_token")
                }
            }
        )
        if (!response.ok) {
            console.error("Users API error:", response.status )
            throw new Error(`HTTP ${response.status}`)
        }
        const data = await response.json()

        if (!Array.isArray(data)) {
            throw new Error("Users API did not return an array")
        }
        users.value = data
    } catch (error) {
        console.error("Users API error:", error)
        users.value = []
    }
}
async function deleteUser(user) {
    if (!confirm(`Permanently delete ${user.fullname}?`)) return

    try {
        const response = await fetch(
            `http://127.0.0.1:5000/api/admin_dashboard/users/${user.user_id}`,
            {
                method: "DELETE",
                headers: {
                    "Authentication-Token": localStorage.getItem("auth_token")
                }
            }
        )

        const data = await response.json()

        if (!response.ok) {
            alert(data.message || "Could not delete user")
            return
        }

        alert("User deleted successfully")
        await getUsers()
    } catch (error) {
        console.error(error)
        alert("Could not connect to the server")
    }
}



const filteredUsers = computed(() => {
    const text = search.value.trim().toLowerCase()

    return users.value.filter(user => {

        const status = user.status ? 'active' : 'inactive'

        const matchesStatus = status.includes(text) &&
        (
            !['active', 'inactive'].includes(text) ||
            status === text
        )

        return (
            String(user.fullname ?? '').toLowerCase().includes(text) ||
            String(user.username ?? '').toLowerCase().includes(text) ||
            String(user.email ?? '').toLowerCase().includes(text) ||
            matchesStatus
        )
})
})

async function changeStatus(id, active) {
    await fetch(
        `http://127.0.0.1:5000/api/admin_dashboard/users/${id}/status`,
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

    getUsers()
}

onMounted(() => {
    getUsers()
})


</script>