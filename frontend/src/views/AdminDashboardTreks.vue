<template>
    <DashNavbar />

    <div class="d-flex">
        <AdminSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Treks</h1>
                <RouterLink to="/admin_dashboard/treks/add_trek" class="btn btn-success"> + Add New Trek </RouterLink>
            </div>

            <div class="input-group mb-4">
                <input
                    type="text"
                    class="form-control"
                    placeholder="Search treks..."
                    v-model="search"
                >
                <button class="btn btn-outline-secondary"> 🔍 </button>
            </div>

            <table class="table table-bordered table-hover align-middle">
                <thead class="table-light">
                    <tr>
                        <th>ID</th>
                        <th>Trek Name</th>
                        <th>Location</th>
                        <th>Difficulty</th>
                        <th>Slots</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="trek in filteredTreks"
                        :key="trek.trek_id"
                    >
                        <td>{{ trek.trek_id }}</td>
                        <td>{{ trek.trek_name }}</td>
                        <td>{{ trek.location }}</td>
                        <td>{{ trek.difficulty }}</td>
                        <td>{{ trek.slots }}</td>

                        <td>
                            <span
                                class="badge"
                                :class="trek.status=='Open'
                                    ? 'bg-success'
                                    : 'bg-danger'"
                            >
                                {{ trek.status }}
                            </span>
                        </td>

                        <td>
                            <button class="btn btn-sm btn-warning me-2"> ✏️ </button>

                            <button class="btn btn-sm btn-danger"> 🗑️ </button>
                        </td>

                    </tr>
                </tbody>
            </table>
        </main>
    </div>

</template>



<script setup>
import { ref, computed, onMounted } from "vue";
import DashNavbar from '@/components/DashNavbar.vue'
import AdminSidebar from '@/components/AdminSidebar.vue';
import { useRouter } from 'vue-router'; // 1. Import it
const router = useRouter(); // 2. Define it

const search = ref("")
const treks = ref([])

async function getTreks(){

    const response = await fetch(
        "http://127.0.0.1:5000/api/admin_dashboard/treks",
        {
            headers:{
                "Authentication-Token":
                    localStorage.getItem("auth_token")
            }
        }
    )
    treks.value = await response.json()
}

onMounted(()=>{
    getTreks()
})

const filteredTreks = computed(()=>{
    return treks.value.filter(trek=>

        trek.trek_name
            .toLowerCase()
            .includes(search.value.toLowerCase())
    )
})

</script>