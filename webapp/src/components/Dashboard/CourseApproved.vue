<template>
  <div class="container" style="margin-top: 2em">
    <!-- ongoing -->
    <div v-if="ongoing.length > 0" class="row">
      <h3>My Current Courses</h3>
      <div v-for="aClass in ongoing" :key="aClass.id" class="card col-4">
        <div class="card-top">
          <!-- name of the course -->
          <h6>{{ aClass.course_name }}</h6>
          <!-- class section -->
          <p class="card-body">G{{ aClass.class_name }}</p>
        </div>
        <div class="card-bottom">
          <div class="progress">
            <div
              class="progress-bar"
              role="progressbar"
              aria-valuenow="{{aClass.progress}}"
              aria-valuemin="0"
              aria-valuemax="100"
            ></div>
          </div>
          <p>{{ aClass.progress }}% completed</p>
        </div>
      </div>
    </div>

    <!-- upcoming -->
    <div v-if="upcoming.length > 0" class="row">
      <h3>My Upcoming Courses</h3>
      <div v-for="aClass in upcoming" :key="aClass.id" class="card col-4">
        <div class="card-top">
          <!-- name of the course -->
          <h6>{{ aClass.course_name }}</h6>
          <!-- class section -->
          <p class="card-body">G{{ aClass.class_name }}</p>
        </div>
        <div class="card-bottom">
          <p>Starting on: {{ convertIS8601Date(aClass.class_start_date) }}</p>
        </div>
      </div>
    </div>

    <!-- past -->
    <div v-if="past.length > 0" class="row">
      <h3>Past Courses</h3>
      <div v-for="aClass in past" :key="aClass.id" class="card col-4">
        <div class="card-top">
          <!-- name of the course -->
          <h6>{{ aClass.course_name }}</h6>
          <!-- class section -->
          <p class="card-body">G{{ aClass.class_name }}</p>
        </div>
        <div class="card-bottom">
          <p>Ended on: {{ convertIS8601Date(aClass.class_end_date) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  name: 'CourseApproved',
  props: {
    past: {
      type: Array,
      required: true,
    },
    ongoing: {
      type: Array,
      required: true,
    },
    upcoming: {
      type: Array,
      required: true,
    },
  },
  methods: {
    convertIS8601Date(dateString) {
      const momentDate = moment.parseZone(dateString).local();
      return momentDate.format('DD MMM YYYY');
    },
  },
};
</script>

<style lang="scss" scoped>
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

.card {
  margin-bottom: 2em;
  margin-right: 2em;
  padding: 14px 16px;
  min-height: 100px;

  display: flex;
  align-content: space-between;
  text-decoration: none;
  color: black;

  h6 {
    margin: 0;
    margin-bottom: 12px;

    font-size: 1em;
    font-weight: bold;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  p {
    margin: 0;
  }

  .card-body {
    --lh: 1.4em;
    --max-lines: 3;

    padding: 0;
    line-height: var(--lh);
    max-height: calc(var(--lh) * var(--max-lines));

    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: var(--max-lines);
    overflow: hidden;
    text-overflow: ellipsis;

    color: $gray-900;
  }

  .card-top {
    padding-bottom: 1em;
  }

  .card-bottom {
    color: $gray-700;
  }
}
</style>
