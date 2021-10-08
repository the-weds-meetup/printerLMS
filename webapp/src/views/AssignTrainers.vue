<template>
  <div class="container-fluid">
    <AssignTrainers />
  </div>
</template>

<script>
// @ is an alias to /src
import AssignTrainers from '@/components/AssignTrainers.vue';

export default {
  name: 'AssignTrainersView',
  components: {
    AssignTrainers,
  },
};
</script>
