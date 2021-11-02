<template>
  <a class="card">
    <div class="card-top">
      <!-- name of the course -->
      <h6>{{ courseName }}</h6>
      <!-- class section -->
      <p class="card-body">{{ classId }}</p>
    </div>
    <!-- either progress bar or class end date -->
    <div class="card-bottom">
      <div class="progress">
        <div
          class="progress-bar"
          role="progressbar"
          style="width: 25%"
          aria-valuenow="{{progess}}"
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
      <p>{{ classEndDate }}</p>
    </div>
  </a>
</template>

<script>
export default {
  name: 'CourseApproved',
  props: {
    courseName: {
      type: String,
      required: true,
    },
    classId: {
      type: Number,
      required: true,
    },
    progress: {
      type: Number,
      required: true,
    },
    classEndDate: {
      type: String,
      required: true,
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
  text-decoration: none;
  color: black;

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
