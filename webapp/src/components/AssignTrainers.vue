<template>
  <div id="main-container" class="container">
    <form :style="{ paddingTop: '20px' }">
      <div class="form-group mb-3">
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
          <option v-for="course in courses" :key="course.id" :value="course.id">
            {{ course.name }}
          </option>
        </select>
      </div>

      <div class="form-group mb-3">
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

      <div class="form-group mb-3">
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
          user_id == 0 || course_id == 0 || class_id == 0 || classes.length == 0
        "
        @click="assignTrainer"
      >
        Assign Trainer
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AssignTrainers',
  data() {
    return {
      trainers: [],
      courses: [],
      classes: [],
      learners_completion: [],
      user_id: 0,
      course_id: 0,
      class_id: 0,
      selected_trainer: [],
      department_id: 2,
      error: '',
      isDisable: '',
    };
  },
  watch: {
    course_id: function () {
      //get classes according to course selected
      axios
        .get(
          'http://localhost:5000/api/classes/get_classes_by_course/' +
            parseInt(this.course_id)
        )
        .then((response) => {
          this.classes = response.data.data;
          //reset class_id whenever a new course is selected
          this.class_id = 0;
        })
        .catch((error) => alert(error));

      //get user_id of learners who have completed the selected course
      axios
        .get(
          'http://localhost:5000/api/learnercompletion/get_learners_by_course/' +
            parseInt(this.course_id)
        )
        .then((response) => {
          this.learners_completion = response.data.data;
          //reset trainers array whenever new course is selected
          this.trainers = [];
          this.user_id = 0;
          for (var each_learner of this.learners_completion) {
            axios
              .get(
                'http://localhost:5000/api/learners/get_trainers_by_id/' +
                  parseInt(each_learner.user_id)
              )
              .then((response) => {
                this.trainers = this.trainers.concat(response.data.data);
              })
              .catch((error) => alert(error));
          }
        });
    },
  },
  mounted: function () {
    axios
      .get('http://localhost:5000/api/course/get_courses')
      .then((response) => {
        this.courses = response.data.data;
      })
      .catch((error) => alert(error));
  },
  methods: {
    assignTrainer: function () {
      axios
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
