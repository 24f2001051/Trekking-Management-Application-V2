<template>
    <DashNavbar />

    <div class="d-flex">
        <AdminSidebar />

        <main class="flex-grow-1 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Add a Staff</h1>
            </div>

            <div class="form-body col-6">                     <!-- form-body -->
    
                <form v-on:submit.prevent="staff_register">
                    <div class="mb-3">
                        <label for="Inputfullname" class="form-label">Staff Name:</label>
                        <input type="text" class="form-control" id="Inputfullname" placeholder="input staff name here"  v-model="fullname" @input="validateFullname">
                        <div class="text-danger">{{ fullnameError }}</div>
                    </div>
                    <div class="mb-3">
                        <label for="InputUsername" class="form-label">Username:</label>
                        <input type="text" class="form-control" id="InputUsername" placeholder="input username here" v-model="username" @input="validateUsername">
                        <div class="text-danger">{{ usernameError }}</div>
                    </div>
                    <div class="mb-3">
                        <label for="InputEmail" class="form-label">Email:</label>
                        <input type="email" class="form-control" id="InputEmail" placeholder="input email here" v-model="email" @input="validateEmail">
                        <div class="text-danger">{{ emailError }}</div>
                    </div>
                    <div class="mb-3">
                        <label for="InputPassword" class="form-label">Password:</label>
                        <input type="password" class="form-control" id="InputPassword" placeholder="password here" v-model="password" @input="validatePassword">
                        <div class="text-danger">{{ passwordError }}</div>
                    </div>

                    <div class="mb-3">
                        <label for="InputPhonenumber" class="form-label">Phone Number:</label>
                        <input type="phone" class="form-control" id="InputPhonenumber" placeholder="phone number" v-model="phonenumber" @input="validatePhonenumber">
                        <div class="text-danger">{{ phonenumberError }}</div>
                    </div>

                    <div class="mb-3">
                        <label for="InputExperience" class="form-label">Experience(yrs):</label>
                        <input type="number" class="form-control" id="InputExperience" placeholder="Staff Experience" v-model="experience" @input="validateExperience">
                        <div class="text-danger">{{ experienceError }}</div>
                    </div>



                    <div class="mb-3">
                        <label for="InputDesignation" class="form-label">Designation:</label>
                        <select id="InputDesignation" class="form-select" placeholder="Select Designation" v-model="designation" @change="ValidateDesignation">                             
                            
                            <option value="" disabled selected >Select Designation</option>
                            <option value="Guide">Guide</option>
                            <option value="Coordinator">Coordinator</option>
                            <option value="Driver">Driver</option>
                                                                                      
                        </select>
                        <div class="text-danger">{{ designationError }}</div>
                    </div>

                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <button type="button" class="btn btn-primary fw-bold" @click="router.push('/admin_dashboard/staff')">Back</button>
                        <input type="submit" class="btn btn-success fw-bold" value="Create Staff">    
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


const fullname = ref('');
const username = ref('');
const email = ref('');
const password = ref('');
const experience = ref('');
const phonenumber = ref('');
const designation = ref('');

const fullnameError = ref('');
const usernameError = ref('');
const emailError = ref('');
const passwordError = ref('');
const experienceError = ref('');
const phonenumberError = ref('');
const designationError = ref('');

    // validation
    const validatePassword = () => {
        if (password.value.length < 1){
            passwordError.value = 'Password cannot be empty!';
            return false;
        } else {
            passwordError.value = '';
            return true;
        } ;
    }
    const validateUsername = () => {
        if (username.value.length < 1){
            usernameError.value = 'Please enter the Username!';
            return false;
        } else {
            usernameError.value = '';
            return true;
        } ;
    }
    const validateEmail = () => {
        if (email.value.length < 1){
            emailError.value = 'Please enter the Email!';
            return false;
        } else {
            emailError.value = '';
            return true;
        } ;
    }
    const validateFullname = () => {
        if (fullname.value.length < 1){
            fullnameError.value = 'Staff name cannot be empty!';
            return false;
        } else {
            fullnameError.value = '';
            return true;
        } ;
    }
    const validateExperience = () => {
        if (experience.value.length < 1){
            experienceError.value = 'Experience cannot be empty!';
            return false;
        } else {
            experienceError.value = '';
            return true;
        } ;
    }
    const validatePhonenumber = () => {
        if (phonenumber.value.length < 1){
            phonenumberError.value = 'Phone number cannot be empty!';
            return false;
        } else {
            phonenumberError.value = '';
            return true;
        } ;
    }
    const ValidateDesignation = () => {
        if (designation.value.length < 1){
            designationError.value = 'Designation cannot be empty!';
            return false;
        } else {
            designationError.value = '';
            return true;
        } ;
    }

    async function staff_register() {

        if (username.value === '' || password.value === '' || email.value === '' || fullname.value === '' || experience.value === '' || phonenumber.value === '' || designation.value === '') {
            alert('Please fill all the fields');
            return;
        }
        
        const token = localStorage.getItem('auth_token');
        const response = await fetch('http://127.0.0.1:5000/api/admin_dashboard/staff/add_staff', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({
                fullname: fullname.value,
                username: username.value,
                email: email.value,
                password: password.value,
                experience: experience.value,
                phonenumber: phonenumber.value,
                designation: designation.value,

            })
        });

        console.log(response)

            if (!response.ok) {
                const errorData = await response.json();
                console.error(errorData);
                alert(`Registration failed: ${errorData.message}`);
                return;
            } else {
                const data = await response.json();
                console.log(data);
        
                router.push('/admin_dashboard/staff');
                return;
            }
        
    }

</script>
<!-- 222222222222222222222222222222222222222222 -->
