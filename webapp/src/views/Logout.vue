<template>
  <div class="container-fluid">
    <p>Logging out...</p>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

export default {
  name: 'Home',
  async mounted() {
    await axios
      .post('/api/auth/logout', {
        token: window.localStorage.getItem('session_token'),
      })
      .catch((error) => {
        console.error(error.response.data.result.message);
      })
      .then(() => {
        // remove everything
        window.localStorage.clear();

        // navigate to login after 5 secs
        setTimeout(function () {
          window.location.replace('/login');
        }, 5000);
      });
  },
};
</script>
