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

        <!-- Course Pre-req  -->
        <div v-if="course.prerequisites.length > 0" class="prereq">
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
            <ol>
              <li v-for="precourse in course.prerequisites" :key="precourse.id">
                {{ precourse.name }}
              </li>
            </ol>
          </div>
        </div>

        <!-- Ongoing classes  -->
        <div class="ongoing-class">
          <div class="header">
            <h4>{{ course.class.enrolling.length }} classes available</h4>
            <button v-if="isAdmin" class="btn">+ Add Class</button>
          </div>

          <p v-if="!isPrereqFulfilled" class="text-danger">
            You are not allowed to enroll until you finish the prerequisites
            courses required
          </p>
          <div v-if="course.class.enrolling.length > 0" class="classes">
            <ClassCard
              v-for="enroll in course.class.enrolling"
              :key="enroll.class_id"
              :class-id="enroll.class_id"
              :course-id="enroll.course_id"
              :max-capacity="enroll.max_capacity"
              :class-start-date="enroll.class_start_date"
              :class-end-date="enroll.class_end_date"
              :enrolment-start-date="enroll.enrolment_start_date"
              :enrolment-end-date="enroll.enrolment_end_date"
              :trainer="enroll.trainer"
              :can-enroll="isPrereqFulfilled && !isCourseCompleted"
            />
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
import ClassCard from '@/components/Course/ClassCard.vue';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';

export default {
  name: 'Home',
  components: {
    SideNav,
    TopNav,
    ClassCard,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      course: undefined,
      classEnrolStatus: undefined,
      isDataFetched: false,
      isPrereqShown: false,
      isPrereqFulfilled: false,
      isCourseCompleted: false,
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
      })
      .catch((error) => {
        console.error(error);
        return undefined;
      });

    // to check if allowed to enrol in course
    await axios
      .post('/api/course/' + this.$route.params.id, {
        token: window.localStorage.getItem('session_token'),
      })
      .then((response) => {
        const data = response.data;
        // prereqs not met, show error message for prereqs
        if (!data.success) {
          this.isPrereqFulfilled = false;
          return;
        } else {
          this.isPrereqFulfilled = true;
          if (data.results.completed) {
            this.isCourseCompleted = true;
          }
        }
        this.isEnrolCheckFinished = true;
      })
      .catch((error) => {
        console.error(error);
      });
    this.isDataFetched = true;
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
  padding-bottom: 16px;

  button {
    font-size: 1.1em;
    font-weight: 600;
    margin-bottom: 24px;
  }
}

.ongoing-class {
  .header {
    display: flex;
    flex-direction: row;

    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;

    h4 {
      font-size: 1.3em;
      font-weight: 600;
      margin: 0;
    }

    .btn {
      font-size: 1.1em;
      font-weight: 600;
      color: $primary;
    }

    .btn:hover {
      text-decoration: underline;
    }
  }
}
</style>
