<template>
  <div class="card" @click.self.prevent="">
    <div class="card-top">
      <h6>{{ title }}</h6>
      <p class="card-body">{{ description }}</p>
    </div>
    <div class="card-bottom">
      <p v-if="numOfClass === 1">{{ numOfClass }} class available</p>
      <p v-else>{{ numOfClass }} classes available</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  props: {
    title: {
      type: String,
      required: true,
    },
    courseId: {
      type: Number,
      required: true,
    },
    description: {
      type: String,
      required: false,
      default: '',
    },
    numOfClass: {
      type: Number,
      required: false,
      default: 0,
    },
  },
};
</script>

<style lang="scss" scoped>
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

.card {
  margin-bottom: 1em;
  padding: 14px 16px;
  min-height: 100px;

  display: flex;
  align-content: space-between;

  h6 {
    margin: 0;
    margin-bottom: 12px;

    font-size: 1em;
    font-weight: bold;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  p {
    margin: 0;
  }

  .card-body {
    --lh: 1.4em;
    --max-lines: 3;

    padding: 0;
    line-height: var(--lh);
    max-height: calc(var(--lh) * var(--max-lines));

    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: var(--max-lines);
    overflow: hidden;
    text-overflow: ellipsis;

    color: $gray-900;
  }

  .card-top {
    padding-bottom: 1em;
  }

  .card-bottom {
    color: $gray-700;
  }
}

.card:hover {
  cursor: pointer;
  border-color: $primary;
}
</style>
