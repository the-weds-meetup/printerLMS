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
    name: 'EnrolCourse',
    component: () => import('../views/Course/EnrolCourse.vue'),
  },
  {
    path: '/class/approve-enrolment',
    name: 'Approve Learner Self-Enrolment',
    component: () => import('../views/Class/ClassApproval.vue'),
  },
  {
    path: '/class/:id/edit',
    name: 'Edit Class',
    component: () => import('../views/Class/ClassEdit.vue'),
  },
  {
    path: '/course/:id/add-class',
    name: 'Add Class',
    component: () => import('../views/Class/ClassAdd.vue'),
  },
  {
    path: '/class/:id/learners',
    name: 'View Class Learners',
    component: () => import('../views/Class/ClassLearners.vue'),
  },
  {
    path: '/class/:id/learners/add',
    name: 'Add Learners to Class',
    component: () => import('../views/Class/ClassLearnersAdd.vue'),
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin/Admin.vue'),
  },
  {
    path: '/admin/assign/trainers',
    name: 'AssignTrainers',
    component: () => import('../views/Admin/AssignTrainers.vue'),
  },
  {
    path: '/admin/assign/learners',
    name: 'ViewAvailableClasses',
    component: () => import('../views/Admin/ViewClasses.vue'),
  },
  {
    path: '/admin/assign/learners/:id',
    name: 'AssignLearners',
    component: () => import('../views/Admin/AssignLearners.vue'),
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
