import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/about',
            name: 'about',
            // route level code-splitting
            // this generates a separate chunk (About.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import('../views/AboutView.vue')
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegisterView.vue')
        },
        {
            path: '/admin_dashboard',
            name: 'admin_dashboard',
            component: () => import('../views/AdminDashboard.vue')
        },
        {
            path: '/staff_dashboard',
            name: 'staff_dashboard',
            component: () => import('../views/StaffDashboard.vue')
        },
        {
            path: '/trekker_dashboard',
            name: 'trekker_dashboard',
            component: () => import('../views/TrekkerDashboard.vue')
        },
        {
            path: '/admin_dashboard/treks',
            name: 'admin_dashboard_treks',
            component: () => import('../views/AdminDashboardTreks.vue')
        },
        {
            path: '/admin_dashboard/staff',
            name: 'admin_dashboard_staff',
            component: () => import('../views/AdminDashboardStaff.vue')
        },
        {
            path: '/admin_dashboard/treks/add_trek',
            name: 'admin_add_treks',
            component: () => import('../views/AddTrek.vue')
        },
        {
            path: '/admin_dashboard/staff/add_staff',
            name: 'staff_register',
            component: () => import('../views/StaffRegisterView.vue')
        },
    ]
})

export default router