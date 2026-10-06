<template>
<DashNavbar />
    <div class="container-fluid">
        <div class="row justify-content-center">
            <div class="form-body col-6">                     <!-- form-body -->
                <br>
                <h3 class= "text-center">Add a Trek</h3>
    
                <form v-on:submit.prevent="saveTrek">
                    <div class="mb-3">
                        <label for="InputTrekname" class="form-label">Trek Name:</label>
                        <input type="text" class="form-control" id="InputTrekname" placeholder="input trek name here" required v-model="trekname" @input="validateTrekname">
                        <div class="text-danger">{{ treknameError }}</div>
                    </div>
                    <div class="mb-3">
                        <label for="InputUsername" class="form-label">Username:</label>
                        <input type="text" class="form-control" id="InputUsername" placeholder="input username here" required v-model="username" @input="validateUsername">
                        <div class="text-danger">{{ usernameError }}</div>
                    </div>
                    <div class="mb-3">
                        <label for="InputEmail" class="form-label">Email:</label>
                        <input type="email" class="form-control" id="InputEmail" placeholder="input email here" required v-model="email" @input="validateEmail">
                        <div class="text-danger">{{ emailError }}</div>
                    </div>
                    <div class="mb-3">
                        <label for="InputPassword" class="form-label">Password:</label>
                        <input type="password" class="form-control" id="InputPassword" placeholder="and password here" required v-model="password" @input="validatePassword">
                        <div class="text-danger">{{ passwordError }}</div>
                    </div>

                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <button type="button" class="btn btn-primary fw-bold" @click="router.push('/admin_dashboard/treks')">Back</button>
                        <input type="submit" class="btn btn-success fw-bold" value="Save">    
                    </div>
                </form>
            </div>
        </div>
    </div>

    </template>
    
<script setup>
    import PublicNavbar from '../components/PublicNavbar.vue'
    import { useRouter } from 'vue-router'; // 1. Import it
    const router = useRouter(); // 2. Define it

    import { ref } from 'vue';
import DashNavbar from '@/components/DashNavbar.vue';

    const fullname = ref('');
    const username = ref('');
    const email = ref('');
    const password = ref('');

    const fullnameError = ref('');
    const usernameError = ref('');
    const emailError = ref('');
    const passwordError = ref('');

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
            fullnameError.value = 'Full name cannot be empty!';
            return false;
        } else {
            fullnameError.value = '';
            return true;
        } ;
    }

    async function register() {

        if (username.value === '' || password.value === '' || email.value === '' || fullname.value === '') {
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
                fullname: fullname.value,
                username: username.value,
                email: email.value,
                password: password.value
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
        
                router.push('/login');
                return;
            }
        
    }

</script>