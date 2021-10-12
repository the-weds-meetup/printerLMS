<template>
  <div class="container-fluid">
    <AssignTrainers />
  </div>
</template>

<script>
// @ is an alias to /src
import AssignTrainers from '@/components/AssignTrainers.vue';

export default {
  name: 'AssignTrainersView',
  components: {
    AssignTrainers,
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
