<template>
  <div class="container-fluid">
    <p>Logging out...</p>
  </div>
</template>

<script>
// @ is an alias to /src
import { cleanupSession } from '@/assets/js/authentication.js';

export default {
  name: 'Home',
  async created() {
    await cleanupSession();
  },
};
</script>
