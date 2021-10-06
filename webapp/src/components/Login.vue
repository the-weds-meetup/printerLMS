<template>
  <form @submit.prevent>
    <div class="form-group login-form">
      <h1 class="mt-5 mb-5">All-in-One LMS</h1>
      <input
        v-model.trim="email"
        class="form-control mb-3"
        placeholder="Email"
        type="email"
      />
      <input
        v-model="password"
        type="password"
        class="form-control mb-3"
        placeholder="Password"
      />

      <button class="btn btn-primary" @click="handleLogin(email, password)">
        Login
      </button>

      <p v-if="isError" class="mt-3 text-danger">{{ error }}</p>
    </div>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      isError: false,
      error: '',
    };
  },
  methods: {
    async handleLogin(email, password) {
      // Create JSON object to receive the auth
      if (email == '' || password == '') {
        this.isError = true;
        this.error = 'Empty fields';
        return;
      }

      await axios
        .post('/api/auth/login', {
          email: email,
          password: password,
        })
        .then((response) => {
          this.isError = false;
          const auth = response.data.result.records[0];
          const expiry_seconds = Date.parse(auth.expiry_date);

          // Save to localstorage, so that it can be used to identify users
          window.localStorage.setItem('session_token', auth.token);
          window.localStorage.setItem('token_expiry', expiry_seconds);
          console.log(expiry_seconds);

          // redirect to dashboard
          window.location.replace('/');
        })
        .catch((error) => {
          this.isError = true;
          this.error = error.response.data.result.message;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.login-form {
  margin: 0 auto;
  height: 100%;
  max-width: 720px;
  display: flex;
  align-content: center;
  justify-content: center;
  flex-direction: column;
}

.btn {
  width: fit-content;
  align-self: center;
}
</style>
