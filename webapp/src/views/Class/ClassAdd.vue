<template>
  <div class="body">
    <!-- Start of navbar -->
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <!-- End of navbar -->
    <main>
      <TopNav title="Add Class" />
      <div id="content" class="content-container">
        <div class="container-fluid">
          <div>
            <!-- Start of form -->

            <form class="center" @submit.prevent="submitform()">
              <div class="form-group">
                <label for="maxCapacityInput" class="form-label"
                  >Max Capacity</label
                >
                <input
                  id="maxCapacityInput"
                  v-model="max_capacity"
                  type="number"
                  placeholder="Max Capacity"
                  class="form-control"
                  min="0"
                />
              </div>

              <!-- Class Dates -->
              <div class="form-group">
                <label for="startDateInput" class="form-label"
                  >Start Date</label
                >
                <input
                  id="startDateInput"
                  v-model="class_start_date"
                  type="datetime-local"
                  placeholder="Start Date"
                  :onchange="onSelectStartDate()"
                  class="form-control"
                  step="3600"
                />
              </div>

              <div class="form-group">
                <label for="endDateInput" class="form-label">End Date</label>
                <input
                  id="endDateInput"
                  v-model="class_end_date"
                  type="datetime-local"
                  placeholder="Start Date"
                  class="form-control"
                  :onchange="onSelectEndDate()"
                  :min="getMinDate1"
                  step="3600"
                />
              </div>

              <!-- Enrolment Dates -->
              <div class="form-group">
                <label for="enrolmentStartDateInput" class="form-label"
                  >Enrolment Start Date</label
                >
                <input
                  id="enrolmentStartDateInput"
                  v-model="enrolment_start_date"
                  type="datetime-local"
                  placeholder="Start Date"
                  class="form-control"
                  :onchange="onSelectEnrolmentStartDate()"
                  step="3600"
                />
              </div>

              <div class="form-group">
                <label for="enrolmentEndDateInput" class="form-label"
                  >End Date</label
                >
                <input
                  id="enrolmentEndDateInput"
                  v-model="enrolment_end_date"
                  type="datetime-local"
                  placeholder="Start Date"
                  class="form-control"
                  :onchange="onSelectEnrolmentEndDate()"
                  :min="getMinDate2"
                  step="3600"
                />
              </div>

              <button class="mt-3 btn btn-primary" type="submit" name="submit">
                Submit
              </button>
            </form>

            <!-- End of form -->
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import moment from 'moment-timezone';

import { checkSessionToken } from '@/assets/js/authentication.js';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';

export default {
  name: 'Createclass',
  components: {
    SideNav,
    TopNav,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      max_capacity: '',
      class_start_date: '',
      class_end_date: '',
      enrolment_start_date: '',
      enrolment_end_date: '',
    };
  },
  computed: {
    // trimStartDate()
    getMinDate1() {
      const date = moment(this.class_start_date)
        .hour(0)
        .minute(0)
        .second(0)
        .millisecond(0);
      return date.format('YYYY-MM-DDTHH:mm:ss');
    },
    getMinDate2() {
      const date = moment(this.enrolment_start_date)
        .hour(0)
        .minute(0)
        .second(0)
        .millisecond(0);
      return date.format('YYYY-MM-DDTHH:mm:ss');
    },
  },
  async created() {
    await checkSessionToken().then(() => {
      this.email = window.sessionStorage.getItem('learner_email');
      this.fullName = window.sessionStorage.getItem('learner_fullname');
      this.isAdmin = window.sessionStorage.getItem('learner_isAdmin') == 'true';
    });
  },
  methods: {
    getISOString(dateString) {
      var date = moment(dateString);
      return date.toISOString();
    },
    onSelectStartDate() {
      const date = moment(this.class_start_date)
        .minute(0)
        .second(0)
        .millisecond(0);
      this.class_start_date = date.format('YYYY-MM-DDTHH:mm:ss');
    },
    onSelectEndDate() {
      const date = moment(this.class_end_date)
        .minute(0)
        .second(0)
        .millisecond(0);
      this.class_end_date = date.format('YYYY-MM-DDTHH:mm:ss');
    },
    onSelectEnrolmentStartDate() {
      const date = moment(this.enrolment_start_date)
        .minute(0)
        .second(0)
        .millisecond(0);
      this.enrolment_start_date = date.format('YYYY-MM-DDTHH:mm:ss');
    },
    onSelectEnrolmentEndDate() {
      const date = moment(this.enrolment_end_date)
        .minute(0)
        .second(0)
        .millisecond(0);
      this.enrolment_end_date = date.format('YYYY-MM-DDTHH:mm:ss');
    },
    submitform() {
      /* console.log("Class created and updated to database!") */
      axios
        .post('http://localhost:5000/api/class', {
          course_id: this.$route.params.id,
          max_capacity: this.max_capacity,
          class_start_date: this.getISOString(this.class_start_date),
          class_end_date: this.getISOString(this.class_end_date),
          enrolment_start_date: this.getISOString(this.enrolment_start_date),
          enrolment_end_date: this.getISOString(this.enrolment_end_date),
        })
        .then(() => {
          this.$router.push('/course/' + this.$route.id);
          return false;
        })
        .catch((error) => {
          this.error = error.response.data.message;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';

.form-group {
  padding: 8px 0;
}
</style>
