<template>
  <form>
    <div class="form-group">
      Course ID:
      <input v-model="id" type="number" placeholder="id" class="form-control" />
    </div>

    <div class="form-group">
      Course Name:
      <input
        v-model="name"
        type="text"
        placeholder="Name"
        class="form-control"
      />
    </div>

    <div class="form-group">
      Course Description:
      <input
        v-model="description"
        type="text"
        placeholder="description"
        class="form-control"
      />
    </div>

    <div class="form-group">
      Course is retired:
      <select v-model="is_retired" class="form-control">
        <option disabled value="">Please select one</option>
        <option>True</option>
        <option>False</option>
      </select>
    </div>

    <button class="btn btn-primary" @click="SubmitCourse">
      Enter New Course
    </button>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SubmitCourse',
  data() {
    return {
      id: '',
      name: '',
      description: '',
      is_retired: False,
    };
  },
  methods: {
    SubmitCourse: function () {
      event.preventDefault();
      axios
        .post('http://localhost:5000/course', {
          id: this.id,
          name: this.name,
          description: this.description,
          is_retired: this.is_retired,
        })
        .then((response) => {
          window.location.replace('localhost/submitcourse');
          return false;
        })
        .catch((error) => {
          this.error = error.response.data.message;
        });
    },
  },
};
</script>
