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
                // Admin Dahboard Routes
        {
            path: '/admin_dashboard',
            name: 'admin_dashboard',
            component: () => import('../views/AdminDashboard.vue')
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
            path: '/admin_dashboard/users',
            name: 'admin_dashboard_users',
            component: () => import('../views/AdminDashboardUsers.vue')
        },
        {
            path: '/admin_dashboard/scheduled_treks',
            name: 'admin_dashboard_scheduled_treks',
            component: () => import('../views/AdminDashboardScheduledTreks.vue')
        },
        {
            path: '/admin_dashboard/bookings',
            name: 'admin_dashboard_bookings',
            component: () => import('../views/AdminDashboardBookings.vue')
        },
        {
            path: '/admin_dashboard/reports',
            name: 'admin_dashboard_reports',
            component: () => import('../views/AdminDashboardReports.vue')
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
        {
            path: '/admin_dashboard/treks/:id/edit',
            name: 'edit_trek',
            component: () => import('../views/EditTrek.vue')
        },
        {
            path: '/admin_dashboard/staff/:id/edit_staff',
            name: 'edit_staff',
            component: () => import('../views/EditStaff.vue')
        },
        {
            path: '/admin_dashboard/treks/:trek_id/schedule',
            name: 'schedule_trek',
            component: () => import('../views/AdminScheduleTrek.vue')
        },

                    // Staff Dashboard Routes
        {
            path: '/staff_dashboard',
            name: 'staff_dashboard',
            component: () => import('../views/StaffDashboard.vue')
        },
        {
            path: '/staff_dashboard/my_trek',
            name: 'staff_my_treks',
            component: () => import('../views/StaffDashboardMyTrek.vue')
        },
        {
            path: '/staff_dashboard/participants',
            name: 'staff_participants',
            component: () => import('../views/StaffDashboardParticipants.vue')
        },
        {
            path: '/staff_dashboard/profile',
            name: 'staff_profile',
            component: () => import('../views/StaffDashboardProfile.vue')
        },
        {
            path: '/staff_dashboard/availability/:id',
            name: 'staff_update_availability',
            component: () => import('../views/StaffUpdateAvailability.vue')
        },
        {
            path: '/staff_dashboard/manage_trek',
            name: 'staff_manage_trek',
            component: () => import('../views/StaffManageTrek.vue'),
            meta: { requiresAuth: true, role: 'staff' }
        },



                // Trekker Dashboard Routes
        {
            path: '/trekker_dashboard',
            name: 'trekker_dashboard',
            component: () => import('../views/TrekkerDashboard.vue')
        },
        {
            path: '/trekker_dashboard/browse_trek',
            name: 'trekker_browse_trek',
            component: () => import('../views/TrekkerBrowseTrek.vue')
        },
        {
            path: '/trekker_dashboard/my_booking',
            name: 'trekker_my_bookings',
            component: () => import('../views/TrekkerDashboardMyBooking.vue')
        },
        {
            path: '/trekker_dashboard/history',
            name: 'trekker_history',
            component: () => import('../views/TrekkerDashboardHistory.vue')
        },
        {
            path: '/trekker_dashboard/profile',
            name: 'trekker_profile',
            component: () => import('../views/TrekkerDashboardProfile.vue')
        },
        {
            path: '/trekker_dashboard/history',
            name: 'trekker_history',
            component: () => import('../views/TrekkerDashboardHistory.vue')
        },

    
    ]
})


router.beforeEach((to) => {
    const token = localStorage.getItem('auth_token');
    const role = localStorage.getItem('role');

    if (to.meta.requiresAuth && !token) {
        return next('/login');
    }

    if (to.meta.role && to.meta.role != role) {
        if (!token) {
            return next('/login');
        }

        if (role === 'admin') {
            return next('/admin_dashboard');
        }

        if (role === 'staff') {
            return next('/staff_dashboard');
        }

        if (role === 'trekker') {
            return next('/trekker_dashboard');
        }

        return next('/login');
    }

    return true;
});


export default router;