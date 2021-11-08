<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav
        v-if="isAdmin"
        title="Course Catalog"
        button-title="+ Add a course"
        :button-action="navigateToAddCourse"
      />
      <TopNav v-else title="Course Catalog" />
      <div id="content">
        <OverviewCard
          v-for="course in courses"
          :key="course.id"
          :title="course.name"
          :course-id="course.id"
          :description="course.description"
          :num-of-class="course.class.enrolling.length || 0"
        />
      </div>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

import { checkSessionToken } from '@/assets/js/authentication.js';
import OverviewCard from '@/components/Course/OverviewCard.vue';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';

export default {
  name: 'Home',
  components: {
    SideNav,
    TopNav,
    OverviewCard,
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
    const data = await axios
      .get(process.env.VUE_APP_BACKEND + '/api/course/all')
      .then((response) => response.data.result.records)
      .catch((error) => {
        console.error(error);
        return [];
      });
    this.courses = data;
    console.log(data);
  },
  methods: {
    navigateToAddCourse() {
      window.location.href = '/course/add';
    },
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';
</style>
