<template>
  <div class="profile">
    <div class="image">
      <h3>{{ fullName.charAt(0) }}</h3>
    </div>
    <div class="description">
      <p>{{ fullName }}</p>
      <p id="email">{{ email }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  props: {
    email: {
      type: String,
      required: true,
    },
    fullName: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

.profile {
  width: 100%;
  padding: 32px 0px 8px 0;
  border-bottom: 1px solid lightgray;

  display: flex;
  flex-direction: column;
  align-items: flex-start;

  .image {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background-color: lightslategray;
    font-size: 2em;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: $white;
  }

  h3 {
    margin: 0;
  }

  .description {
    padding-top: 20px;

    p {
      text-align: left;
      margin: 0;
      margin-bottom: 4px;
    }
  }

  #email {
    color: $gray-600;
  }
}
</style>
