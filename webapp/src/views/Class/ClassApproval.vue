<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="Approve Self-Enrolled Learners" />
      <div id="content"></div>
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
  name: 'AllClassApproval',
  components: {
    SideNav,
    TopNav,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      isDataFetched: false,
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
      .get(process.env.VUE_APP_BACKEND + '/api/course/' + this.$route.params.id)
      .then((response) => {
        const data = response.data.result.records;
        this.course = data;
        this.isDataFetched = true;
      })
      .catch((error) => {
        console.error(error);
        return undefined;
      });
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
