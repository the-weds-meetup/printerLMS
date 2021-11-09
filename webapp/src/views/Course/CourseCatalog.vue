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
      <Spinner v-if="!isFetched" />
      <div v-else id="content">
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
import Spinner from '@/components/Tools/Spinner.vue';

export default {
  name: 'Home',
  components: {
    SideNav,
    TopNav,
    Spinner,
    OverviewCard,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      courses: [],
      isFetched: false,
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
      .get(process.env.VUE_APP_BACKEND + '/api/course/all')
      .then((response) => {
        this.courses = response.data.result.records;
        this.isFetched = true;
      })
      .catch((error) => {
        console.error(error);
      });
  },
  methods: {
    navigateToAddCourse() {
      this.$router.push('/course/add');
    },
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';
</style>
