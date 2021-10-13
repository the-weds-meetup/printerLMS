<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="Course" />
      <div v-if="isDataFetched" id="content">
        <div class="description">
          <h1>{{ course.name }}</h1>
          <p>{{ course.description }}</p>
        </div>
        <div class="prereq">
          <button
            class="btn btn-primary"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapsePreq"
            aria-expanded="false"
            aria-controls="collapsePreq"
            @click="togglePrereqButton()"
          >
            <span v-if="!isPrereqShown">Show</span>
            <span v-else>Hide</span>
            Course Pre-requisites
          </button>
          <div id="collapsePreq" class="collapse">
            <p v-if="course.prerequisites.length === 0">nothing</p>
            <ol v-else>
              <li v-for="precourse in course.prerequisites" :key="precourse.id">
                {{ precourse.name }}
              </li>
            </ol>
          </div>
        </div>
      </div>
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
  name: 'Home',
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
  async mounted() {
    await axios
      .get('/api/course/' + this.$route.params.id)
      .then((response) => {
        const data = response.data.result.records;
        this.course = data;
        this.isDataFetched = true;
      })
      .catch((error) => {
        console.error(error);
        return undefined;
      });
  },
  methods: {
    togglePrereqButton() {
      this.isPrereqShown = !this.isPrereqShown;
    },
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

#content {
  h1 {
    font-size: 1.6em;
    font-weight: 600;
    margin-bottom: 24px;
  }

  p {
    color: $gray-800;
    font-size: 1.1em;
  }
}

.description {
  padding-bottom: 12px;
}

.prereq {
  button {
    font-size: 1.1em;
    font-weight: 600;
    margin-bottom: 24px;
  }

  #collapsePreq {
  }
}
</style>
