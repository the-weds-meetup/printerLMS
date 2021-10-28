<template>
  <div class="card">
    <div class="card-top">
      <h5>G{{ classId }}</h5>
      <button v-if="isAdmin" class="btn" @click="navtigateToEditClas()">
        Edit
      </button>
      <button
        v-else
        :disabled="!canEnroll || enrollState !== 'no_enroll'"
        class="btn"
        @click="enrollClass()"
      >
        {{ checkStatus() }}
      </button>
    </div>
    <div class="class-body">
      <div class="row-side">
        <div>
          <h6>Instructor</h6>
          <p>{{ trainer }}</p>
        </div>
        <div class="right-hand">
          <h6>Class Size</h6>
          <p>{{ maxCapacity }}</p>
        </div>
      </div>
      <div class="row">
        <h6>Class Period</h6>
        <p>
          {{ convertIS8601Date(classStartDate) }} -
          {{ convertIS8601Date(classEndDate) }}
        </p>
      </div>
      <div v-if="enrolmentStartDate !== ''" class="row">
        <h6>Enrolment Period</h6>
        <p>
          {{ convertIS8601Date(enrolmentStartDate) }} -
          {{ convertIS8601Date(enrolmentEndDate) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

export default {
  name: 'Profile',
  props: {
    classId: {
      type: Number,
      required: true,
    },
    courseId: {
      type: Number,
      required: true,
    },
    trainer: {
      type: String,
      required: true,
    },
    maxCapacity: {
      type: Number,
      required: true,
    },
    classStartDate: {
      type: String,
      required: true,
    },
    classEndDate: {
      type: String,
      required: true,
    },
    enrolmentStartDate: {
      type: String,
      required: false,
      default: '',
    },
    enrolmentEndDate: {
      type: String,
      required: false,
      default: '',
    },
    canEnroll: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      isAdmin: false,
      enrollState: 'no_enroll',
    };
  },
  async created() {
    this.isAdmin = window.sessionStorage.getItem('learner_isAdmin') == 'true';
  },
  async mounted() {
    await this.learnerEnrollStatus();
  },
  methods: {
    convertIS8601Date(dateString) {
      const momentDate = moment.parseZone(dateString).local();
      return momentDate.format('DD MMM YYYY');
    },
    checkStatus() {
      switch (this.enrollState) {
        case 'approve':
          return 'Approved';
        case 'awaiting_approval':
          return 'Waiting For Approval';
        case 'no_enroll':
        default:
          return 'Enroll';
      }
    },
    async learnerEnrollStatus() {
      await axios
        .post(`/api/class/${this.classId}/status`, {
          token: window.localStorage.getItem('session_token'),
        })
        .then((response) => {
          this.enrollState = response.data.results.status;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    async enrollClass() {
      await axios
        .post(`/api/enroll/self/${this.classId}`, {
          token: window.localStorage.getItem('session_token'),
        })
        .then(() => {
          location.reload();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    navtigateToEditClas() {
      if (this.isAdmin) {
        window.location.href = `/class/${this.classId}/edit`;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

.card {
  margin-bottom: 1em;
  padding: 14px 16px;
  min-height: 100px;

  text-decoration: none;
  color: black;

  h5 {
    margin: 0;
  }

  h6 {
    margin: 0;
    padding-bottom: 4px;
    font-size: 1em;
    font-weight: bold;
  }

  p {
    margin: 0;
  }

  .row,
  .row-side {
    padding-bottom: 12px;
  }

  .row-side {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  .right-hand {
    text-align: right;
  }
}

.card-body {
  padding: 0;
  color: $gray-900;
}

.card-top {
  padding-bottom: 1em;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;

  .btn {
    font-size: 1.1em;
    font-weight: 600;
    color: $primary;
    padding: 0;
  }

  .btn:hover {
    text-decoration: underline;
  }
}
</style>
