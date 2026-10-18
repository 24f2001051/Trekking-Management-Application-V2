<template>
    <DashNavbar />

    <div class="d-flex">
        <TrekkerSidebar />

        <main class="flex-grow-1 p-4">
            <h2 class="fw-bold">My Profile</h2>
            <p class="text-muted mb-4">View and update your profile information.</p>

            <div v-if="message" class="alert"
                :class="messageType === 'success' ? 'alert-success' : 'alert-danger'">
                {{ message }}
            </div>

            <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary"></div>
                <p>Loading profile...</p>
            </div>

            <div v-else-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
                <button class="btn btn-sm btn-outline-danger ms-2" @click="loadProfile">Retry</button>
            </div>

            <div v-else class="card profile-card border-0 shadow-sm">
                <div class="card-body p-4">
                    <div class="profile-avatar mb-3">
                        {{ initials }}
                    </div>

                    <form @submit.prevent="updateProfile">
                        <div class="row g-3">
                            <div class="col-12 col-md-6">
                                <label class="form-label">Full Name *</label>
                                <input v-model.trim="profile.fullname" class="form-control" required maxlength="120">
                            </div>

                            <div class="col-12 col-md-6">
                                <label class="form-label">Username</label>
                                <input :value="profile.username" class="form-control" readonly>
                            </div>

                            <div class="col-12 col-md-6">
                                <label class="form-label">Email</label>
                                <input v-model.trim="profile.email" type="email" class="form-control" required maxlength="120">
                            </div>

                            <div class="col-12 col-md-6">
                                <label class="form-label">Phone Number</label>
                                <input v-model="profile.phone" type="tel" class="form-control" maxlength="15"
                                    inputmode="numeric" pattern="[0-9]{10,15}" placeholder="e.g. 1234567890">
                            </div>

                            <div class="col-12 col-md-6">
                                <label class="form-label">Date of Birth</label>
                                <input v-model="profile.dob" type="date" class="form-control">
                            </div>

                            <div class="col-12 col-md-6">
                                <label class="form-label">Gender</label>
                                <select v-model="profile.gender" class="form-select">
                                    <option value="">Select Gender</option>
                                    <option value="M">Male</option>
                                    <option value="F">Female</option>
                                    <option value="O">Other</option>
                                </select>
                            </div>

                            <div class="col-12">
                                <label class="form-label">Address</label>
                                <textarea v-model="profile.address" class="form-control"
                                    rows="3" maxlength="500" placeholder="e.g. 123 Main Street, City, Country"></textarea>
                            </div>
                        </div>

                        <div class="d-flex flex-wrap gap-2 mt-4">
                            <button type="submit" class="btn btn-primary" :disabled="saving">
                                {{ saving ? 'Saving...' : 'Save Changes' }}
                            </button>

                            <button type="button" class="btn btn-outline-secondary" :disabled="saving" @click="loadProfile">
                                Reset
                            </button>
                        </div>
                    </form>
                </div>
            </div>

        </main>
    </div>

</template>


<script setup>
import { ref, computed , onMounted } from 'vue';
import { useRouter } from 'vue-router'; // 1. Import it
import DashNavbar from '../components/DashNavbar.vue';
import TrekkerSidebar from '../components/TrekkerSidebar.vue';

const router = useRouter(); // 2. Define it

const emptyProfile = () => ({
    trekker_id: null,
    fullname: '',
    username: '',
    email: '',
    phone: '',
    dob: '',
    gender: '',
    address: ''
})

const profile = ref(emptyProfile());
const loading = ref(false);
const saving = ref(false);
const errorMessage = ref('');
const message = ref('');
const messageType = ref('success');

const initials = computed(() => {
    const name = profile.value.fullname.trim();

    if (!name) return 'T';

    return name.split(/\s+/).slice(0, 2).map(part => part[0].toUpperCase()).join('');
});

async function loadProfile() {
    loading.value = true;
    errorMessage.value = '';
    message.value = '';

    try {
        const token = localStorage.getItem('auth_token');

        if (!token) {
            router.push('/login');
            return;
        }

        const response = await fetch('http://127.0.0.1:5000/api/trekker_dashboard/profile', {
            method: 'GET',
            headers: {
                'Authentication-Token': token
            }
        });

        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }

        const data = await response.json();

        profile.value = {
            ...emptyProfile(),
            ...data,
            phone: data.phone || '',
            dob: data.dob || '',
            gender: data.gender || '',
            address: data.address || ''
        }

    } catch (error) {
        console.error('Profile API error:', error);
        errorMessage.value = error.message || 'Unable to load profile';
    } finally {
        loading.value = false;
    }
}

async function updateProfile() {

    if (!profile.value.fullname.trim() || !profile.value.email.trim()) {
        message.value = 'Full name and email are required';
        messageType.value = 'error';
        return;   
    }

    saving.value = true;
    message.value = '';

    try {
        const token = localStorage.getItem('auth_token');

        const response = await fetch('http://127.0.0.1:5000/api/trekker_dashboard/profile', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({
                fullname: profile.value.fullname,
                email: profile.value.email,
                phone: profile.value.phone,
                dob: profile.value.dob,
                gender: profile.value.gender,
                address: profile.value.address
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Unable to update profile');
        }

        localStorage.setItem('fullname', profile.value.fullname);

        message.value = data.message || 'Profile updated successfully';
        messageType.value = 'success';
    
    } catch (error) {
        message.value = error.message || 'Unable to update your profile';
        messageType.value = 'error';
    } finally {
        saving.value = false;
    }
}


onMounted(() => {
    loadProfile();
})
</script>


<style scoped>
.trekker-layout {
    min-height: calc(100vh - 60px);
}

.dashboard-content {
    min-width: 0;
    background: #f8fafc;
}

.profile-card {
    max-width: 900px;
    border-radius: 12px;
}

.profile-avatar {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #dbeafe;
    color: #1d4ed8;
    font-size: 1.5rem;
    font-weight: 700;
}

@media (max-width: 768px) {
    .dashboard-content {
        padding: 1rem !important;
    }
}
</style>

