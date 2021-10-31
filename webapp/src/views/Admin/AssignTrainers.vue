<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="Assign Trainers" />
      <form :style="{ paddingTop: '20px', paddingLeft: '20px' }">
        <div class="form-group col-md-11 mb-3">
          <div :style="{ textAlign: 'left' }">
            <label
              for="selectCourse"
              class="form-label"
              :style="{ display: 'block' }"
            >
              Select Course
            </label>
          </div>
          <select id="selectCourse" v-model="course_id" class="form-select">
            <option
              v-for="course in courses"
              :key="course.id"
              :value="course.id"
            >
              {{ course.name }}
            </option>
          </select>
        </div>

        <div class="form-group col-md-11 mb-3">
          <div :style="{ textAlign: 'left' }">
            <label
              for="selectTrainer"
              class="form-label"
              :style="{ display: 'block' }"
            >
              Select Trainer
            </label>
          </div>
          <select id="selectTrainer" v-model="user_id" class="form-select">
            <option
              v-for="trainer in trainers"
              :key="trainer.user_id"
              :value="trainer.user_id"
            >
              {{ trainer.name }}
            </option>
            <option v-if="trainers.length == 0" disabled>
              No trainers currently available for this course
            </option>
          </select>
        </div>

        <div class="form-group col-md-11 mb-3">
          <div :style="{ textAlign: 'left' }">
            <label
              for="selectClass"
              class="form-label"
              :style="{ display: 'block' }"
            >
              Select Class
            </label>
          </div>
          <select id="selectClass" v-model="class_id" class="form-select">
            <option
              v-for="each_class in classes"
              :key="each_class.id"
              :value="each_class.id"
            >
              G{{ each_class.class_id }}:
              {{ convertIS8601Date(each_class.class_start_date) }} -
              {{ convertIS8601Date(each_class.class_end_date) }}
            </option>
            <option v-if="classes.length == 0" disabled>
              No classes currently available for this course
            </option>
          </select>
        </div>

        <button
          type="button"
          class="btn btn-primary"
          :disabled="
            user_id == 0 ||
            course_id == 0 ||
            class_id == 0 ||
            classes.length == 0
          "
          @click="assignTrainer"
        >
          Assign Trainer
        </button>
      </form>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

// @ is an alias to /src
import { checkSessionToken } from '@/assets/js/authentication.js';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';

export default {
  name: 'AssignTrainers',
  components: {
    SideNav,
    TopNav,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      trainers: [],
      courses: [],
      classes: [],
      user_id: 0,
      course_id: 0,
      class_id: 0,
    };
  },
  watch: {
    course_id: async function () {
      //get classes according to course selected
      await axios
        .get('http://localhost:5000/api/course/' + parseInt(this.course_id))
        .then((response) => {
          //reset classes and trainers of previous query
          this.classes = [];
          this.class_id = 0;
          this.trainers = [];
          this.user_id = [];

          // display enrolling classes which would not have a trainer assigned yet
          var enrol_classes = response.data.result.records.class.enrolling;

          for (var each_class of enrol_classes) {
            this.classes = this.classes.concat(each_class);
          }

          var past_classes = response.data.result.records.class.past;

          for (var each_past_class of past_classes) {
            this.getTrainers(each_past_class);
          }
        })
        .catch((error) => {
          console.log(error);
          this.classes = [];
        });

      console.log(this.trainers);
    },
  },
  async created() {
    await checkSessionToken().then(() => {
      this.email = window.sessionStorage.getItem('learner_email');
      this.fullName = window.sessionStorage.getItem('learner_fullname');
      this.isAdmin = window.sessionStorage.getItem('learner_isAdmin') == 'true';
    });
  },
  mounted: async function () {
    await axios
      .get('/api/course/all')
      .then((response) => {
        this.courses = response.data.result.records;
      })
      .catch((error) => alert(error));
  },
  methods: {
    convertIS8601Date(dateString) {
      const momentDate = moment.parseZone(dateString).local();
      return momentDate.format('DD MMM YYYY');
    },

    getTrainers: async function (each_past_class) {
      await axios
        .get('/api/class/' + parseInt(each_past_class.id))
        .then((response) => {
          this.trainers = this.trainers.concat(
            response.data.result.records.past_learners
          );
        })
        .catch((error) => alert(error));
    },

    assignTrainer: async function () {
      await axios
        .post('/api/trainer/add', {
          user_id: this.user_id,
          class_id: this.class_id,
        })
        .then((response) => {
          alert(response.data.message);
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';
</style>
