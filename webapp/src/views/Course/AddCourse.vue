<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav
        v-if="isAdmin"
        title="Add a New Course"
        button-title="Save"
        :button-action="onSubmit"
      />
      <TopNav v-else title="Add a New Course" />
      <form id="content">
        <!-- Course Name -->
        <div class="form-group">
          <label for="course-name" class="form-label">Course Name</label>
          <input
            id="course-name"
            v-model.trim="courseName"
            type="text"
            placeholder="Course Name"
            class="form-control"
          />
          <p v-if="errorName" class="error">{{ errorName }}</p>
        </div>

        <!-- Course Description -->
        <div class="form-group">
          <label for="course-description" class="form-label"
            >Course Description</label
          >
          <textarea
            id="course-description"
            v-model.trim="courseDescription"
            type="text"
            placeholder="A brief description of the course"
            class="form-control"
            rows="5"
          />
          <p v-if="errorDescription" class="error">{{ errorDescription }}</p>
        </div>

        <!-- Retire course -->
        <fieldset id="retire-course">
          <label class="form-label">Hide Course?</label>
          <div class="form-check">
            <input
              id="radio-no"
              v-model="isRetire"
              class="form-check-input"
              type="radio"
              name="retire-course"
              value="false"
              checked
            />
            <label class="form-check-label" for="radio-no">No</label>
          </div>
          <div class="form-check">
            <input
              id="radio-yes"
              v-model="isRetire"
              class="form-check-input"
              type="radio"
              name="retire-course"
              value="true"
            />
            <label class="form-check-label" for="radio-yes">Yes</label>
          </div>
        </fieldset>

        <!-- Course Prereqs -->
        <fieldset v-if="courseList.length > 0" id="get-preqs">
          <label class="form-label">Course Pre-requisites</label>

          <div v-for="course in courseList" :key="course.id" class="form-check">
            <input
              :id="'radio-' + course.id"
              v-model="coursePreReqs"
              class="form-check-input"
              type="checkbox"
              :value="course.id"
            />
            <label class="form-check-label" :for="'radio-' + course.id">
              {{ course.name }}
            </label>
          </div>
        </fieldset>
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
      courseName: '',
      courseDescription: '',
      isRetire: 'false',
      coursePreReqs: [],
      courseList: [],
      errorName: undefined,
      errorDescription: undefined,
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
    this.courseList = await axios
      .get(process.env.VUE_APP_BACKEND + '/api/course/all')
      .then((response) => {
        const data = response.data.result.records;
        return data;
      })
      .catch((error) => {
        console.error(error);
        return [];
      });
  },
  methods: {
    async onSubmit() {
      let isNamePassed = false;
      let isDescriptionPassed = false;

      if (this.courseName.length > 0) {
        isNamePassed = true;
        this.errorName = undefined;
      } else {
        this.errorName = 'Course Name is required';
      }

      if (this.courseDescription.length > 0) {
        isDescriptionPassed = true;
        this.errorDescription = undefined;
      } else {
        this.errorDescription = 'Course Description is required';
      }

      if (!this.coursePreReqs) {
        this.coursePreReqs = [];
      }

      if (isNamePassed && isDescriptionPassed) {
        await axios
          .post(process.env.VUE_APP_BACKEND + '/api/course/add', {
            token: window.localStorage.getItem('session_token'),
            name: this.courseName,
            description: this.courseDescription,
            is_retired: this.isRetire == 'true',
            prerequisites: this.coursePreReqs,
          })
          .then(() => {
            this.$router.push('/catalog');
          })
          .catch((error) => {
            console.log(error);
            window.alert(error.response.result.message);
          });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

.form-label {
  font-weight: 600;
}

.form-group {
  margin-bottom: 16px;
}

.form-check {
  margin-bottom: 8px;
}

#retire-course {
  margin-bottom: 16px;
}

.error {
  padding-top: 4px;
  color: $red;
}
</style>
