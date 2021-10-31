<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav
        title="Learners"
        button-title="+ Add Learner"
        @click="navigateToAdd"
      />
      <div id="content">
        <Spinner v-if="!isDataFetched" />

        <div v-else>
          <ol>
            <li v-for="learner in learners" :key="learner.id">
              {{ learner.full_name }}
            </li>
          </ol>
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
import Spinner from '@/components/Tools/Spinner.vue';

export default {
  name: 'EditCourse',
  components: {
    SideNav,
    TopNav,
    Spinner,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      isDataFetched: false,
      learners: [],
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
    this.learners = await axios
      .get(`/api/class/${this.$route.params.id}/learners`)
      .then((response) => {
        this.isDataFetched = true;
        return response.data.results.records;
      })
      .catch((error) => {
        console.error(error);
      });
  },
  methods: {
    togglePrereqButton() {
      this.isPrereqShown = !this.isPrereqShown;
    },
    navigateToAdd() {
      if (this.isAdmin) {
        window.location.href = `/class/${this.$route.params.id}/learners/add`;
      }
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

li {
  padding: 8px 0;
}
</style>
