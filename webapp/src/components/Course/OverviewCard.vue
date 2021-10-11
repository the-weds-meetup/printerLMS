<template>
  <div class="card">
    <h6>{{ title }}</h6>
    <p class="card-body">{{ description }}</p>
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
  },
};
</script>

<style lang="scss" scoped>
@import '~bootstrap/scss/bootstrap';

.card {
  margin-bottom: 1em;
  padding: 14px 16px;
  min-height: 100px;

  h6 {
    margin: 0;
    margin-bottom: 12px;

    font-size: 1em;
    font-weight: bold;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.card:hover {
  cursor: pointer;
  border-color: $primary;
}

.card-body {
  --lh: 1.4em;
  --max-lines: 3;

  margin: 0;
  padding: 0;
  line-height: var(--lh);
  max-height: calc(var(--lh) * var(--max-lines));

  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: var(--max-lines);
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
