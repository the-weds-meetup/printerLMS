<template>
  <nav class="top-nav">
    <h1>{{ title }}</h1>
  </nav>
</template>

<script>
export default {
  name: 'TopNav',
  components: {},
  props: {
    title: {
      type: String,
      default: '',
      required: false,
    },
  },
};
</script>

<style lang="scss" scoped>
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

.top-nav {
  height: 64px;
  padding: 0 24px;
  width: 100%;

  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: $gray-200;

  h1 {
    font-size: 1.5em;
    margin: 0;
  }
}
</style>
