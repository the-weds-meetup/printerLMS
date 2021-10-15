<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="Add a New Course" />
      <form id="content">
        <div class="form-group">
          Course ID:
          <input
            v-model="id"
            type="number"
            placeholder="id"
            class="form-control"
          />
        </div>

        <div class="form-group">
          Course Name:
          <input
            v-model="name"
            type="text"
            placeholder="Name"
            class="form-control"
          />
        </div>

        <div class="form-group">
          Course Description:
          <input
            v-model="description"
            type="text"
            placeholder="description"
            class="form-control"
          />
        </div>

        <div class="form-group">
          Course is retired:
          <select v-model="is_retired" class="form-control">
            <option disabled value="">Please select one</option>
            <option>True</option>
            <option>False</option>
          </select>
        </div>

        <button class="btn btn-primary" @click="SubmitCourse">
          Enter New Course
        </button>
      </form>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

import { checkSessionToken } from '@/assets/js/authentication.js';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';

export default {
  name: 'AddCourse',
  components: {
    SideNav,
    TopNav,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      isDataFetched: false,
      isPrereqShown: false,
      course: undefined,
    };
  },
  async created() {
    await checkSessionToken().then(() => {
      this.email = window.sessionStorage.getItem('learner_email');
      this.fullName = window.sessionStorage.getItem('learner_fullname');
      this.isAdmin = window.sessionStorage.getItem('learner_isAdmin') == 'true';
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
