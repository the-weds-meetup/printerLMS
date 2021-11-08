<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav :title="title" />
      <Spinner v-if="!isDataFetched" />
      <div v-else id="content" class="container-fluid">
        <!-- ClassHeader -->
        <ClassHeader
          :course-name="currentClass.course_name"
          :class-name="currentClass.class_id"
          :current-capacity="countLearners"
          :max-capacity="currentClass.max_capacity"
        />
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

import { checkSessionToken } from '@/assets/js/authentication.js';
import ClassHeader from '@/components/Class/ClassHeader.vue';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';
import Spinner from '@/components/Tools/Spinner.vue';

export default {
  name: 'AssignerLearners',
  components: {
    SideNav,
    TopNav,
    Spinner,
    ClassHeader,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      isDataFetched: false,
      max_capacity: 0,
      currentClass: undefined,
    };
  },
  computed: {
    countLearners() {
      return this.currentClass.learners.length || 0;
    },
    title() {
      if (!this.currentClass) {
        return 'A Default Class';
      }
      return `${this.currentClass.course_name} G(${this.currentClass.class_id})`;
    },
  },
  async created() {
    await checkSessionToken().then(() => {
      this.email = window.sessionStorage.getItem('learner_email');
      this.fullName = window.sessionStorage.getItem('learner_fullname');
      this.isAdmin = window.sessionStorage.getItem('learner_isAdmin') == 'true';
    });
  },
  async mounted() {
    await this.populateData();
  },
  methods: {
    async populateData() {
      this.isDataFetched = false;
      await axios
        .post(
          process.env.VUE_APP_BACKEND + `/api/class/${this.$route.params.id}`,
          {
            token: window.localStorage.getItem('session_token'),
          }
        )
        .then((response) => {
          this.currentClass = response.data.result.records;
        })
        .catch((error) => alert(error.response.data.result.message));

      this.isDataFetched = true;
    },
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';
</style>
