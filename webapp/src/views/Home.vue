<template>
<<<<<<< HEAD
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
=======
  <div class="container-fluid">
    <HelloWorld />
>>>>>>> main
  </div>
</template>

<script>
// @ is an alias to /src
<<<<<<< HEAD
import HelloWorld from '@/components/HelloWorld.vue'
=======
import HelloWorld from '@/components/HelloWorld.vue';
>>>>>>> main

export default {
  name: 'Home',
  components: {
<<<<<<< HEAD
    HelloWorld
  }
}
=======
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
>>>>>>> main
</script>
