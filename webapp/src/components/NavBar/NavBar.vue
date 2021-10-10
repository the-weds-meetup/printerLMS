<template>
  <nav class="navigation">
    <Profile :email="email" :full-name="fullName" />

    <div class="link">
      <router-link to="/">Dashboard</router-link>
      <router-link to="/">My Courses</router-link>
      <router-link to="/">Course Catalog</router-link>
      <router-link to="/">Messages</router-link>
      <router-link v-if="isAdmin" to="/">Site Administration</router-link>
      <router-link to="/">Logout</router-link>
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
.navigation {
  width: 350px;
  padding: 0 24px;
  box-sizing: border-box;

  display: flex;
  flex-direction: column;
  align-items: flex-start;

  border-right: 1px solid lightgray;
}

.link {
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  padding: 8px 0;
}
</style>
