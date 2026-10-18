<template>
    <DashNavbar />

    <div class="d-flex">
        <AdminSidebar />

        <main class="flex-grow-1 p-4">
            <h2> Edit Staff </h2>
            
            <form @submit.prevent="updateStaff">
                <div class="mb-3">
                    <label class="form-label">Full Name:</label>
                    <input v-model="staff.fullname" type="text" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Username:</label>
                    <input v-model="staff.username" type="text" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Email:</label>
                    <input v-model="staff.email" type="email" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Designation:</label>
                    <select v-model="staff.designation" class="form-select" required>
                        <option value="" disabled>Select Designation</option>
                        <option value="Guide">Guide</option>
                        <option value="Coordinator">Coordinator</option>
                        <option value="Driver">Driver</option>
                    </select>
                </div>

                <div class="mb-3">
                    <label class="form-label">Experience (in yrs):</label>
                    <input v-model.number="staff.experience_years" type="number" class="form-control" min="0" max="60" step="1" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Date of Birth:</label>
                    <input v-model="staff.dob" type="date" class="form-control" >
                </div>

                <div class="mb-3">
                    <label class="form-label">Phone Number:</label>
                    <input v-model="staff.phone" type="tel" class="form-control" >
                </div>

                <div class="mb-3">
                    <label class="form-label">Gender:</label>
                    <select v-model="staff.gender" class="form-select" >
                        <option value="" disabled>Select Gender</option>
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                        <option value="O">Other</option>
                    </select>
                </div>



                <div class="mb-3">
                    <label class="form-label">Address:</label>
                    <textarea v-model="staff.address" class="form-control" rows="3" ></textarea>
                </div>

                <button type="button" class="btn btn-secondary me-2" @click="router.push('/admin_dashboard/staff')">
                    back
                </button>

                <button type="submit" class="btn btn-success" :disabled="saving">
                    {{ saving ? 'Updating...' : 'Update Staff' }}
                </button>
            </form>

        </main>
    </div>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AdminSidebar from '../components/AdminSidebar.vue';
import DashNavbar from '../components/DashNavbar.vue';

const route = useRoute();
const router = useRouter();

const saving = ref(false);

const staff = ref({
    fullname: '',
    username: '',
    email: '',
    dob: '',
    phone: '',
    gender: '',
    address: '',
    experience_years: 0,
    designation: ''
});

async function getStaff() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/admin_dashboard/staff/${route.params.id}/edit_staff`, {

            headers: {
                'Authentication-Token': localStorage.getItem('auth_token')
            }
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.message || 'Failed to fetch staff details');
            return;
        }

        staff.value = {
            fullname: data.fullname ?? '',
            username: data.username ?? '',
            email: data.email ?? '',
            dob: data.dob ?? '',
            phone: data.phone == null ? '' : String(data.phone),
            gender: data.gender ?? '',
            address: data.address ?? '',
            experience_years: data.experience_years ?? 0,
            designation: data.designation ?? ''
        }

    } catch (error) {
        console.error('Error fetching staff:', error);
        alert('Failed to fetch staff details');
    }
}

async function updateStaff() {
    if (saving.value) return

    saving.value = true

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/admin_dashboard/staff/${route.params.id}/edit_staff`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth_token')
            },
            body: JSON.stringify({
                fullname: staff.value.fullname.trim(),
                username: staff.value.username.trim(),
                email: staff.value.email.trim(),
                dob: staff.value.dob,
                phone: staff.value.phone,
                gender: staff.value.gender,
                address: staff.value.address,
                experience_years: staff.value.experience_years,
                designation: staff.value.designation
            })
        });
        const data = await response.json();

        if (!response.ok) {
            alert(data.message || 'Failed to update staff');
            return
        }

        alert(data.message || 'Staff updated successfully');
        router.push('/admin_dashboard/staff');

    } catch (error) {
        console.error('Error updating staff:', error);
        alert('Unable to connect to the server');
    } finally {
        saving.value = false
    }
}

onMounted(() => {
    getStaff();
});


</script>