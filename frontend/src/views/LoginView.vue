<template>
    <PublicNavbar />
<div class="container-fluid">
    <div class="row justify-content-center">
        <div class="form-body col-6">                     <!-- form-body -->
            <h3 class= "text-center">Login</h3>

            <form v-on:submit.prevent="login">
                <div class="mb-3">
                    <label for="InputUsername" class="form-label">Username:</label>
                    <input type="text" class="form-control" id="InputUsername" placeholder="input username here" required v-model="username" @input="validateUsername">
                    <div class="text-danger">{{ usernameError }}</div>
                </div>
                <div class="mb-3">
                    <label for="InputPassword" class="form-label">Password:</label>
                    <input type="password" class="form-control" id="InputPassword" placeholder="and password here" required v-model="password" @input="validatePassword">
                    <div class="text-danger">{{ passwordError }}</div>
                </div>
                <div class="text">
                    <input type="submit" class="btn btn-primary fw-bold" value="Login">
                    <br>Don't have an account? <a class="text-sign" type="button" href="/register">Register</a>
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


    const username = ref('');
    const password = ref('');

    const usernameError = ref('');
    const passwordError = ref('');

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

    async function login() {

        if (username.value === '' || password.value === '') {
            alert('Please fill all the fields');
            return;
        }
        
        const response = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value
            })
        });

        console.log(response)

        if (!response.ok) {
            const errorData = await response.json();
            console.error(errorData);
            alert(`Login failed: ${errorData.message}`);
            return;
        } else {
            const data = await response.json();
            console.log(data);

            localStorage.setItem('auth_token', data.auth_token);
            localStorage.setItem('role', data.user_detail.role[0]);
            localStorage.setItem('id', data.user_detail.id);
            localStorage.setItem('username', data.user_detail.username);
            localStorage.setItem('fullname', data.user_detail.fullname);
            localStorage.setItem('email', data.user_detail.email);

            const role = data.user_detail.role[0];

            if (role === 'admin') {
                router.push('/admin_dashboard');
            }else if (role === 'staff') {
                router.push('/staff_dashboard');
            }else if (role === 'trekker') {
                router.push('/trekker_dashboard');
            }

            // router.push('/');
            return;
        }

    }

</script>