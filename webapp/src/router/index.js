import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
  },
  {
    path: '/catalog',
    name: 'Course Catalog',
    component: () => import('../views/Course/CourseCatalog.vue'),
  },
  {
    path: '/course/add',
    name: 'Add Course',
    component: () => import('../views/Course/AddCourse.vue'),
  },
  {
    path: '/course/:id',
    name: 'Course',
    component: () => import('../views/Course/Course.vue'),
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
  },
  {
    path: '/messages',
    name: 'Messages',
    component: () => import('../views/Messages.vue'),
  },
  {
    path: '/me',
    name: 'Profile',
    component: () => import('../views/Profile/Profile.vue'),
  },
  {
    path: '/me/course',
    name: 'MyCourses',
    component: () => import('../views/Profile/Course.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Auth/Login.vue'),
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import('../views/Auth/Logout.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
