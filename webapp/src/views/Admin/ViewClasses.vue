<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="Assign Learners to Class" />
      <div id="content">
        <ClassEnrol
          v-for="enrol in classes"
          :key="enrol.id"
          :class-id="enrol.id"
          :class-name="enrol.class_id"
          :course-name="enrol.course_name"
          :current-capacity="enrol.current_capacity"
          :max-capacity="enrol.max_capacity"
        />
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

import { checkSessionToken } from '@/assets/js/authentication.js';
import ClassEnrol from '@/components/Course/ClassEnrol.vue';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';

export default {
  name: 'AllClassEnrolling',
  components: {
    SideNav,
    TopNav,
    ClassEnrol,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      classes: [],
      isDataFetched: false,
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
      .get(process.env.VUE_APP_BACKEND + '/api/course/enrol')
      .then((response) => {
        const data = response.data.results.records;
        this.classes = data;
        this.isDataFetched = true;
      })
      .catch((error) => {
        console.error(error.response.data);
      });
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';
</style>
