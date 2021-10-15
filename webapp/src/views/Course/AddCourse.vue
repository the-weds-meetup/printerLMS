<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav v-if="isAdmin" title="Add a New Course" button-title="Save" />
      <TopNav v-else title="Add a New Course" />
      <form id="content">
        <!-- Course Name -->
        <div class="form-group">
          <label for="course-name" class="form-label">Course Name</label>
          <input
            id="course-name"
            v-model="courseName"
            type="text"
            placeholder="Course Name"
            class="form-control"
          />
        </div>

        <!-- Course Description -->
        <div class="form-group">
          <label for="course-description" class="form-label"
            >Course Description</label
          >
          <textarea
            id="course-description"
            v-model="courseDescription"
            type="text"
            placeholder="A brief description of the course"
            class="form-control"
            rows="5"
          />
        </div>

        <!-- Retire course -->
        <fieldset id="retire-course">
          <label class="form-label">Hide Course?</label>
          <div class="form-check">
            <input
              id="radio-no"
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
      isRetire: false,
      coursePreReqs: [],
      courseList: [],
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
      .get('/api/course/all')
      .then((response) => {
        const data = response.data.result.records;
        console.log(data);
        return data;
      })
      .catch((error) => {
        console.error(error);
        return [];
      });
  },
  methods: {},
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
</style>
