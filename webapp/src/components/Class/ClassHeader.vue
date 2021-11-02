<template>
  <div class="description">
    <div class="name">
      <h1>
        {{ courseName }}
      </h1>
      <h3>{{ `G${className}` }}</h3>
    </div>
    <div class="enrol-count">
      <div class="enrol-container">
        <h1>
          {{ `${currentCapacity} / ${maxCapacity}` }}
        </h1>
        <p>students enrolled</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClassHeader',
  props: {
    courseName: {
      type: String,
      required: true,
    },
    className: {
      type: Number,
      required: true,
    },
    currentCapacity: {
      type: Number,
      required: false,
      default: 0,
    },
    maxCapacity: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

.description {
  display: flex;
  flex-direction: row;

  h1,
  h3,
  p {
    margin: 0;
  }

  .name {
    flex: 2;
    h1 {
      font-size: 2em;
    }

    h3 {
      margin-top: 8px;
      font-size: 1.8em;
    }
  }

  .enrol-count {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
    font-size: 1.2em;

    .enrol-container {
      text-align: center;
      background-color: $gray-300;
      padding: 4px 24px;
      border-radius: 8px;
    }

    h3 {
      font-size: 1.8em;
      margin-bottom: 8px;
    }
  }
}

.learners {
  margin-top: 3em;
}
</style>
