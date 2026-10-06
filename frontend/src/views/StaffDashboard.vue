<template>
    <DashNavbar />
    <div class="container mt-5">
        <h1>{{ role }} Dashboard</h1>
    

    </div>

</template>

<script setup>
import DashNavbar from '../components/DashNavbar.vue'
import { useRouter } from 'vue-router'; // 1. Import it
const router = useRouter(); // 2. Define it

const role = localStorage.getItem('role');
const id = localStorage.getItem('id');
const username = localStorage.getItem('username');
const fullname = localStorage.getItem('fullname');
const email = localStorage.getItem('email');


</script>