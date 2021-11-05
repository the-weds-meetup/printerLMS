<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="My Courses" />
      <Spinner v-if="!learnerCourses" />
      <div v-else id="content">
        <div
          :v-if="isTrainer"
          class="btn-group"
          role="group"
          aria-label="Basic radio toggle button group"
        >
          <input
            id="courseselect1"
            v-model="selected"
            type="radio"
            class="btn-check"
            name="btnradio"
            autocomplete="off"
            value="class-learner"
            checked
          />
          <label class="btn btn-outline-primary" for="courseselect1"
            >Student</label
          >

          <input
            id="courseselect2"
            v-model="selected"
            type="radio"
            class="btn-check"
            name="btnradio"
            autocomplete="off"
            value="class-trainer"
          />
          <label class="btn btn-outline-primary" for="courseselect2"
            >Trainer</label
          >
        </div>
        <!-- Learner -->
        <LearnerView
          v-if="selected === 'class-learner'"
          :past="learnerCourses.past"
          :ongoing="learnerCourses.ongoing"
          :upcoming="learnerCourses.upcoming"
        />

        <!-- Trainer -->
        <TrainerView
          v-else-if="selected === 'class-trainer'"
          :past="trainerCourses.past"
          :ongoing="trainerCourses.ongoing"
          :upcoming="trainerCourses.upcoming"
        />
      </div>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

import { checkSessionToken } from '@/assets/js/authentication.js';
import CourseApproved from '@/components/Course/CourseApproved.vue';
import LearnerView from '@/components/Dashboard/LearnerView.vue';
import TrainerView from '@/components/Dashboard/TrainerView.vue';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';
import Spinner from '@/components/Tools/Spinner.vue';

export default {
  name: 'MyCourses',
  components: {
    CourseApproved,
    SideNav,
    Spinner,
    TopNav,
    LearnerView,
    TrainerView,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      courses: [],
      selected: 'class-learner',
      learnerCourses: undefined,
      trainerCourses: undefined,
    };
  },
  computed: {
    isTrainer() {
      console.log(this.trainerCourses);
      if (
        this.trainerCourses &&
        Object.keys(this.trainerCourses) > 0 &&
        (this.trainerCourses.past.length > 0 ||
          this.trainerCourses.upcoming.length > 0 ||
          this.trainerCourses.ongoing.length > 0)
      ) {
        return true;
      }
      return false;
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
    await axios
      .post('/api/enrollment/approved', {
        token: window.localStorage.getItem('session_token'),
      })
      .then((response) => {
        console.log(response);
      });
      axios.post('/api/me/classes', {
        token: window.localStorage.getItem('session_token'),
      })
      .then((response) => {
        const data = response.data.results.records;
        this.learnerCourses = data.learner;
        this.trainerCourses = data.trainer;
      })
      .catch((error) => {
        console.error(error.response.data.message);
      });

    console.log(this.learnerCourses, this.trainerCourses);
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';

.show-courses {
  margin-top: 1em;
}
</style>
