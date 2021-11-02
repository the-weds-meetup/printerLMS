<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="Manage Learners" />
      <Spinner v-if="!isDataFetched" />
      <div v-else id="content" class="container-fluid">
        <!-- Description -->
        <div class="description">
          <div class="name">
            <h1>
              {{ currentClass.course_name }}
            </h1>
            <h3>{{ `G${currentClass.class_id}` }}</h3>
          </div>
          <div class="enrol-count">
            <div class="enrol-container">
              <h1>
                {{ `${countLearners} / ${currentClass.max_capacity}` }}
              </h1>
              <p>students enrolled</p>
            </div>
          </div>
        </div>

        <!-- Table  -->
        <div class="learners">
          <h4>All Self-Enrolments</h4>
          <table class="table table-striped">
            <thead>
              <tr>
                <th scope="col">Name</th>
                <th scope="col">Email</th>
                <th scope="col">Department</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="learner in waitingList" :key="learner.id">
                <td>{{ learner.full_name }}</td>
                <td>{{ learner.email }}</td>
                <td>{{ learner.department }}</td>
                <td v-if="!isAdding">
                  <button
                    class="btn btn-primary"
                    @click="enrolLearner(learner.id)"
                  >
                    Approve
                  </button>
                </td>
                <td v-else><Spinner /></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

import { checkSessionToken } from '@/assets/js/authentication.js';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';
import Spinner from '@/components/Tools/Spinner.vue';

export default {
  name: 'AssignerLearners',
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
      isAdding: false,
      max_capacity: 0,
      waitingList: [],
      currentClass: undefined,
    };
  },
  computed: {
    countLearners() {
      return this.currentClass.learners.length || 0;
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
        .get(`/api/class/${this.$route.params.id}`)
        .then((response) => {
          this.currentClass = response.data.result.records;
        })
        .catch((error) => alert(error.response.data));

      await axios
        .get(
          `http://localhost:5000/api/class/${this.$route.params.id}/waiting-list`
        )
        .then((response) => {
          this.waitingList = response.data.results.records;
        })
        .catch((error) => {
          console.error(error.response.data);
        });
      this.isDataFetched = true;
    },
    async enrolLearner(learner_id) {
      this.isAdding = true;
      console.log(learner_id);
      await axios
        .post(`/api/enroll/manual/${this.$route.params.id}`, {
          token: window.localStorage.getItem('session_token'),
          learners: [learner_id],
        })
        .then(async () => {
          await this.populateData();
        })
        .catch((error) => {
          console.log(error.response.data);
        });
      this.isAdding = false;
    },
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

.description {
  display: flex;
  flex-direction: row;

  h1,
  h3,
  p {
    margin: 0;
  }

  .name {
    flex: 2;
    h1 {
      font-size: 2em;
    }

    h3 {
      margin-top: 8px;
      font-size: 1.8em;
    }
  }

  .enrol-count {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
    font-size: 1.2em;

    .enrol-container {
      text-align: center;
      background-color: $gray-300;
      padding: 4px 24px;
      border-radius: 8px;
    }

    h3 {
      font-size: 1.8em;
      margin-bottom: 8px;
    }
  }
}

.learners {
  margin-top: 3em;
}

td {
  vertical-align: middle;
}
</style>
