<template>
  <div class="container-fluid">
    <Login />
  </div>
</template>

<script>
// @ is an alias to /src
import Login from '@/components/Login.vue';

export default {
  name: 'Home',
  components: {
    Login,
  },
  created() {
    if (
      window.localStorage.getItem('session_token') &&
      window.localStorage.getItem('token_expiry')
    ) {
      window.location.replace('/');
    }
  },
};
</script>
