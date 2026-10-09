<template>
    <DashNavbar />

    <div class="d-flex">
        <AdminSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Add a Trek</h1>
            </div>

            <div class="form-body col-6">                     <!-- form-body -->
    
                <form v-on:submit.prevent="add_trek">
                    <div class="mb-3">
                        <label for="Inputtrekname" class="form-label">Trek Name:</label>
                        <input type="text" class="form-control" id="Inputtrekname" placeholder="input trek name here"  v-model="trekname" @input="validateTrekname">
                        <div class="text-danger">{{ treknameError }}</div>
                    </div>
                    <div class="mb-3">
                        <label for="InputLocation" class="form-label">Location:</label>
                        <input type="text" class="form-control" id="InputLocation" placeholder="input location here" v-model="location" @input="validateLocation">
                        <div class="text-danger">{{ locationError }}</div>
                    </div>
                    <div class="mb-3">
                        <label for="InputDifficulty" class="form-label">Difficulty:</label>
                        <select id="InputDifficulty" class="form-select" placeholder="Choose Difficulty" v-model="difficulty" @change="validateDifficulty">                             
                                                    
                            <option value="" disabled selected >Choose Difficulty</option>
                            <option value="Explorer">Explorer(Beginner)</option>
                            <option value="Adventurer">Adventurer(Intermediate)</option>
                            <option value="Trialblazer">Trialblazer(Advanced)</option>
                                                              
                        </select>
                        <div class="text-danger">{{ difficultyError }}</div>
                    </div>

                    <div class="mb-3">
                        <label for="InputDuration" class="form-label">Duration:</label>
                        <input type="number" class="form-control" id="InputDuration" placeholder="duration here" v-model="duration" @input="validateDuration">
                        <div class="text-danger">{{ durationError }}</div>
                    </div>

                    <div class="mb-3">
                        <label for="InputDescription" class="form-label">Description:</label>
                        <textarea type="text" class="form-control" id="InputDescription" placeholder="write a brief description here" v-model="description" @input="validateDescription"></textarea>
                        <div class="text-danger">{{ descriptionError }}</div>
                    </div>


                    
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <button type="button" class="btn btn-primary fw-bold" @click="router.push('/admin_dashboard/treks')">Back</button>
                        <input type="submit" class="btn btn-success fw-bold" value="Create A Trek">    
                    </div>
                </form>
            </div>

            
        </main>
    </div>

</template>



<script setup>
import { ref, computed, onMounted } from "vue";
import DashNavbar from '@/components/DashNavbar.vue'
import AdminSidebar from '@/components/AdminSidebar.vue';
import { useRouter } from 'vue-router'; // 1. Import it
const router = useRouter(); // 2. Define it



const trekname = ref('');
const location = ref('');
const difficulty = ref('');
const duration = ref('');
const description = ref('');

const treknameError = ref('');
const locationError = ref('');
const difficultyError = ref('');
const durationError = ref('');
const descriptionError = ref('');

    // validation

    const validateTrekname = () => {
        if (trekname.value.length < 1){
            treknameError.value = 'Trek name cannot be empty!';
            return false;
        } else {
            treknameError.value = '';
            return true;
        } ;
    }
    const validateLocation = () => {
        if (location.value.length < 1){
            locationError.value = 'Please enter the Location!';
            return false;
        } else {
            locationError.value = '';
            return true;
        } ;
    }
    const validateDifficulty = () => {
        if (difficulty.value.length < 1){
            difficultyError.value = 'Choose the difficulty!';
            return false;
        } else {
            difficultyError.value = '';
            return true;
        } ;
    }
    const validateDuration = () => {
        if (duration.value === null || duration.value === undefined || duration.value.toString().length < 1){
            durationError.value = 'Mention the duration!';
            return false;
        } else {
            durationError.value = '';
            return true;
        } ;
    }
    const validateDescription = () => {
        if (description.value.length < 1){
            descriptionError.value = 'Give a breif discription!';
            return false;
        } else {
            descriptionError.value = '';
            return true;
        } ;
    }
    

    async function add_trek() {

        if (trekname.value === '' || location.value === '' || difficulty.value === '' || duration.value === '' || description.value === '') {
            alert('Please fill all the fields');
            return;
        }
        
        const token = localStorage.getItem('auth_token');
        const response = await fetch('http://127.0.0.1:5000/api/admin_dashboard/treks/add_trek', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({
                trek_name: trekname.value,
                location: location.value,
                difficulty: difficulty.value,
                duration: duration.value,
                description: description.value,

            })
        });

        console.log(response)

            if (!response.ok) {
                const errorData = await response.json();
                console.error(errorData);
                alert(`Adding a Trek failed: ${errorData.message}`);
                return;
            } else {
                const data = await response.json();
                console.log(data);
        
                router.push('/admin_dashboard/treks');
                return;
            }
        
    }

</script>


