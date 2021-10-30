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
              Max Capacity:
              <input
                v-model="max_capacity"
                type="number"
                placeholder="Max Capacity"
              />
              <br /><br />
              Start Date:
              <input
                v-model="class_start_date"
                type="datetime-local"
                placeholder="Start Date"
                step="3600"
              />
              <button type="button" name="Verify1" @click="getmin1()">
                Verify</button
              ><br /><br />
              End Date:
              <input
                id="setmin1"
                v-model="class_end_date"
                type="datetime-local"
                placeholder="End Date"
                min="2021-10-14T00:00"
                step="3600"
              />
              <br /><br />
              Enrolment Start Date:
              <input
                v-model="enrolment_start_date"
                type="datetime-local"
                placeholder="Enrolment Start Date"
                step="3600"
              />
              <button type="button" name="Verify2" @click="getmin2()">
                Verify</button
              ><br /><br />
              Enrolment End Date:
              <input
                id="setmin2"
                v-model="enrolment_end_date"
                type="datetime-local"
                placeholder="Enrolment End Date"
                min="2021-10-14T00:00"
                step="3600"
              />
              <br /><br />
              <button type="submit" name="submit">Submit</button>
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
import moment from 'moment';

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
  async created() {
    await checkSessionToken().then(() => {
      this.email = window.sessionStorage.getItem('learner_email');
      this.fullName = window.sessionStorage.getItem('learner_fullname');
      this.isAdmin = window.sessionStorage.getItem('learner_isAdmin') == 'true';
    });
  },
  methods: {
    getmin1() {
      console.log('Start Date -> Running');
      console.log(this.class_start_date);
      document
        .getElementById('setmin1')
        .setAttribute('min', this.class_start_date);
    },
    getmin2() {
      console.log('Enrolment Start Date -> Running');
      console.log(this.enrolment_start_date);
      document
        .getElementById('setmin2')
        .setAttribute('min', this.enrolment_start_date);
    },
    getISOString(dateString) {
      var date = moment(dateString);
      return date.toISOString();
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
</style>
