<template>
  <div class="learner-view">
    <div v-if="ongoing.length > 0" class="class">
      <h3>Ongoing Classes</h3>
      <ul>
        <li v-for="aClass in ongoing" :key="aClass.id">
          <a :href="`/class/${aClass.id}`"
            >{{ aClass.course_name }} {{ `(G${aClass.class_id})` }}</a
          >
        </li>
      </ul>
    </div>
    <div v-if="upcoming.length > 0" class="class">
      <h3>Upcoming Classes</h3>
      <li v-for="aClass in upcoming" :key="aClass.id">
        {{ aClass.course_name }} {{ `(G${aClass.class_id})` }}
      </li>
    </div>
    <div v-if="past.length > 0" class="class">
      <h3>Past Classes</h3>
      <li v-for="aClass in past" :key="aClass.id">
        {{ aClass.course_name }} {{ `(G${aClass.class_id})` }}
      </li>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  name: 'LearnerView',
  props: {
    past: {
      type: Array,
      required: true,
    },
    ongoing: {
      type: Array,
      required: true,
    },
    upcoming: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {};
  },
  methods: {
    convertIS8601Date(dateString) {
      const momentDate = moment.parseZone(dateString).local();
      return momentDate.format('DD MMM YYYY');
    },
  },
};
</script>

<style lang="scss" scoped>
@import '~bootstrap/scss/bootstrap';
@import '~bootstrap/scss/_variables.scss';

.learner-view {
  margin: 1.5em 0;

  .class {
    margin-bottom: 1.5em;
  }
}
</style>
