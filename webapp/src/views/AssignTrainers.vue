<template>
  <div id="main-container" class="dashboard">
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
              Recommended Trainers
            </label>
          </div>
          <select id="selectTrainer" v-model="user_id" class="form-select">
            <option
              v-for="trainer in trainers"
              :key="trainer.id"
              :value="trainer.id"
            >
              {{ trainer.first_name }}
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
              :key="each_class.class_id"
              :value="each_class.class_id"
            >
              Class {{ each_class.class_id }}: starting date
              {{ each_class.class_start_date.substring(0, 10) }}
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
      learners_completion: [],
      user_id: 0,
      course_id: 0,
      class_id: 0,
    };
  },
  watch: {
    course_id: async function () {
      //get classes according to course selected
      await axios
        .get(
          'http://localhost:5000/api/classes/get_classes_by_course/' +
            parseInt(this.course_id)
        )
        .then((response) => {
          this.classes = response.data.data;
          //reset class_id whenever a new course is selected
          this.class_id = 0;
        })
        .catch((error) => {
          console.log(error);
          this.classes = [];
        });

      //get user_id of learners who have completed the selected course
      await axios
        .get(
          'http://localhost:5000/api/learnercompletion/get_learners_by_course/' +
            parseInt(this.course_id)
        )
        .then((response) => {
          //reset trainers
          this.user_id = 0;
          this.trainers = [];

          this.learners_completion = response.data.data;
          this.learners_completion = this.learners_completion.sort(
            (a, b) => parseInt(a.user_id) - parseInt(b.user_id)
          );

          // for (var each_learner of this.learners_completion) {
          //   this.getTrainers(each_learner);
          // }

          // this.learners_completion.forEach((each_learner) => {
          //   this.getTrainers(each_learner);
          // });

          this.learners_completion.forEach(this.getTrainers);

          this.trainers = this.trainers.sort(
            (a, b) => parseInt(a.id) - parseInt(b.id)
          );
        })
        .catch((error) => {
          console.log(error);
          this.trainers = [];
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
      .get('http://localhost:5000/api/course/get_courses')
      .then((response) => {
        this.courses = response.data.data;
      })
      .catch((error) => alert(error));
  },
  methods: {
    getTrainers: async function (each_learner) {
      await axios
        .get(
          'http://localhost:5000/api/learners/get_trainers_by_id/' +
            parseInt(each_learner.user_id)
        )
        .then((response) => {
          this.trainers = this.trainers.concat(response.data.data);
        })
        .catch((error) => alert(error));
    },

    assignTrainer: async function () {
      await axios
        .post('http://localhost:5000/api/trainer/assign_trainer', {
          user_id: this.user_id,
          course_id: this.course_id,
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
.dashboard {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: row;
}

main {
  width: calc(100vw - 350px);
  display: flex;
  flex-direction: column;
}
</style>
