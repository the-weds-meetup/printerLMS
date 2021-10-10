<template>
  <nav class="navigation">
    <Profile :email="email" :full-name="fullName" />

    <div id="nav">
      <router-link to="/">Dashboard</router-link>
      <router-link to="/me/course">My Courses</router-link>
      <router-link to="/course/catalog">Course Catalog</router-link>
      <router-link to="/message">Messages</router-link>
      <router-link v-if="isAdmin" to="/admin">Site Administration</router-link>
      <router-link to="/logout">Logout</router-link>
    </div>
  </nav>
</template>

<script>
import Profile from '@/components/NavBar/components/Profile.vue';

export default {
  name: 'NavBar',
  components: {
    Profile,
  },
  props: {
    email: {
      type: String,
      required: true,
    },
    fullName: {
      type: String,
      required: true,
    },
    isAdmin: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
};
</script>

<style lang="scss" scoped>
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

.navigation {
  width: 350px;
  padding: 0 24px;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;
  align-items: flex-start;

  border-right: 1px solid lightgray;
}

#nav {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 8px 0;
}

#nav a {
  width: 100%;
  box-sizing: border-box;
  text-align: left;
  font-weight: bold;
  color: $gray-900;
  padding: 8px 12px;
  border-radius: 4px;
  text-decoration: none;
}

#nav a.router-link-exact-active {
  color: $gray-100;
  background: $primary;
}
</style>
