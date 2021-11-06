<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav
        :title="courseTitle"
        button-title="+ Add Learner"
        :button-action="enrolLearners"
        :is-disabled="checkedNames.length === 0"
      />
      <div id="content">
        <Spinner v-if="!isDataFetched" />

        <div v-else>
          <div v-for="learner in learners" :key="learner.id" class="form-check">
            <input
              :id="'flex-check' + learner.id"
              v-model="checkedNames"
              class="form-check-input"
              type="checkbox"
              :value="learner.id"
            />
            <label class="form-check-label" :for="'flex-check' + learner.id">
              {{ learner.full_name }}
            </label>
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
import Spinner from '@/components/Tools/Spinner.vue';

export default {
  name: 'EditCourse',
  components: {
    SideNav,
    Spinner,
    TopNav,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      isDataFetched: false,
      learners: [],
      checkedNames: [],
    };
  },
  computed: {
    courseTitle() {
      let base = 'Add Learners ';

      if (this.checkedNames.length > 0) {
        base = base + ` (${this.checkedNames.length})`;
      }
      return base;
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
    this.learners = await axios
      .get(`/api/class/${this.$route.params.id}/nonlearners`)
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
    async enrolLearners() {
      if (!this.isAdmin || this.checkedNames.length === 0) {
        return;
      }
      const errorNames = await axios
        .post(`/api/enroll/manual/${this.$route.params.id}`, {
          token: window.localStorage.getItem('session_token'),
          learners: this.checkedNames,
        })
        .then((response) => response.data.results.records)
        .catch((error) => {
          console.error(error);
        });

      if (errorNames) {
        alert('This learners are not added\n' + errorNames.join('\n'));
      } else {
        window.location.href = `/class/${this.$route.params.id}/learners`;
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

.form-check {
  padding-top: 8px;
  padding-bottom: 8px;
  label {
    padding-left: 4px;
  }
}
</style>
