<template>
  <div class="card" @click="handleClick()">
    <div class="card-custom">
      <div class="title">
        {{ `${courseName} (G${className})` }}
      </div>
      <div class="capacity">
        {{ `${currentCapacity} / ${maxCapacity}` }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClassEnrol',
  props: {
    classId: {
      type: Number,
      required: true,
    },
    className: {
      type: Number,
      required: true,
    },
    courseName: {
      type: String,
      required: true,
    },
    currentCapacity: {
      type: Number,
      required: true,
    },
    maxCapacity: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      isAdmin: false,
    };
  },
  methods: {
    handleClick() {
      this.$router.push('/admin/assign/learners/' + this.classId);
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
  min-height: 50px;

  text-decoration: none;
  color: black;

  .card-custom {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  .title {
    font-weight: 600;
  }
}

.card:hover {
  cursor: pointer;
  border-color: $primary;
  color: $primary;
}
</style>
