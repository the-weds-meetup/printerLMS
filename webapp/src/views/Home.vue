<template>
  <div class="container-fluid">
    <HelloWorld />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue';

export default {
  name: 'Home',
  components: {
    HelloWorld,
  },
  created() {
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
    console.log('hi');
  },
};
</script>
