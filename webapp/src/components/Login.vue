<template>
  <div class="login-form">
    <input v-model.trim="email" class="form-control mb-3" placeholder="Email" />
    <input
      v-model="password"
      class="form-control mb-3"
      placeholder="Password"
    />

    <button class="btn" @click="handleLogin">Login</button>

    <p>Message is: {{ email }} {{ password }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    handleLogin: () => {},
  },
};
</script>

<style lang="scss" scoped>
.login-form {
  margin: 0 auto;
  max-width: 720px;
  display: flex;
  align-content: center;
  justify-content: center;
  flex-direction: column;
}

.btn {
  width: fit-content;
}
</style>
