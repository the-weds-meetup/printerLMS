<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="My Courses" />

      <div id="content">
        <h3>My Current Courses</h3>
        <CourseApproved />

        <h3>My Upcoming Courses</h3>
        <CourseApproved />

        <h3>Past Courses</h3>
        <CourseApproved />
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

// @ is an alias to /src
import { checkSessionToken } from '@/assets/js/authentication.js';
import CourseApproved from '@/components/Course/CourseApproved.vue';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';

export default {
  name: 'MyCourses',
  components: {
    CourseApproved,
    SideNav,
    TopNav,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      courses: [],
    };
  },
  async created() {
    await checkSessionToken().then(() => {
      this.email = window.sessionStorage.getItem('learner_email');
      this.fullName = window.sessionStorage.getItem('learner_fullname');
      this.isAdmin = window.sessionStorage.getItem('learner_isAdmin') == 'true';
    });
  },
  async mounted() {
    await axios
      .post('/api/enrollment/approved', {
        token: window.localStorage.getItem('session_token'),
      })
      .then((response) => {
        console.log(response);
      });
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';
</style>
