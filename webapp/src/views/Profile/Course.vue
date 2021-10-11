<template>
  <div class="dashboard">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="My Courses" />
      <h3>Work in Progress</h3>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src
import { checkSessionToken } from '@/assets/js/authentication.js';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';

export default {
  name: 'MyCourses',
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
    await checkSessionToken().then(() => {
      this.email = window.sessionStorage.getItem('learner_email');
      this.fullName = window.sessionStorage.getItem('learner_fullname');
      this.isAdmin = window.sessionStorage.getItem('learner_isAdmin') == 'true';
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
