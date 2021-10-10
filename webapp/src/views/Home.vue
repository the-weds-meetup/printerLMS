<template>
  <div class="dashboard">
    <NavBar :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <HelloWorld />
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

import HelloWorld from '@/components/HelloWorld.vue';
import NavBar from '@/components/NavBar/NavBar.vue';

export default {
  name: 'Home',
  components: {
    HelloWorld,
    NavBar,
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
  width: 100vh;
  height: 100vh;
  display: flex;
  flex-direction: row;
}
</style>
