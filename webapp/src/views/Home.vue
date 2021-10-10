<template>
  <div class="dashboard">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="Dashboard" />
      <h3>Work in Progress</h3>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';

export default {
  name: 'Home',
  components: {
    SideNav,
    TopNav,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
    };
  },
  async created() {
    // if credentials not found, redirect to login screen
    // if expired, redirect to login screen
    if (
      !window.localStorage.getItem('session_token') ||
      !window.localStorage.getItem('token_expiry') ||
      Date.now() >= parseInt(window.localStorage.getItem('token_expiry'))
    ) {
      window.localStorage.clear();
      window.location.replace('/login');
    }

    await axios
      .post('/api/learner', {
        token: window.localStorage.getItem('session_token'),
      })
      .then((response) => {
        const learner = response.data.result.records[0];
        this.fullName = learner.full_name;
        this.email = learner.email;
        this.isAdmin = learner.is_admin;
      })
      .catch((error) => {
        console.error(error.response.data.result.message);
      });
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
