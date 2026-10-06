<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useRouter } from 'vue-router'; // 1. Import it
const router = useRouter(); // 2. Define it
const fullname = localStorage.getItem('fullname');

</script>

<template>
    <div class="container">
        <nav class="navbar navbar-expand-lg bg-body-tertiary"> <!--  NAVBAR Start-->
            <div class="container-fluid">
                <RouterLink class="navbar-brand" to="#">Welcome, {{ fullname }}</RouterLink>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>   
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        
                    </ul>
                    <form class="d-flex" role="search">
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"/>
                        <button class="btn btn-outline-success" type="submit">🔍</button>
                    </form>
                </div>
            </div>


        </nav>  <!--  NAVBAR End -->



        <RouterView />
    </div>
</template>

