<template>
  <div class="body">
    <SideNav :email="email" :full-name="fullName" :is-admin="isAdmin" />
    <main>
      <TopNav title="Site Administration" />
      <div id="content">
        <div
          class="btn-group"
          role="group"
          aria-label="Basic radio toggle button group"
        >
          <input
            id="adminselect1"
            v-model="selected"
            type="radio"
            class="btn-check"
            name="btnradio"
            autocomplete="off"
            value="course"
            checked
          />
          <label class="btn btn-outline-primary" for="adminselect1"
            >Courses</label
          >

          <input
            id="adminselect2"
            v-model="selected"
            type="radio"
            class="btn-check"
            name="btnradio"
            autocomplete="off"
            value="learner"
          />
          <label class="btn btn-outline-primary" for="adminselect2"
            >Learners</label
          >
        </div>
        <div v-if="selected === 'course'" class="content-body">
          <ul>
            <li>
              <a href="/course/management" class="link-primary"
                >Manage Courses and Classes
              </a>
            </li>
            <li>
              <a href="/course/add" class="link-primary">Add a New Course</a>
            </li>
          </ul>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src
import { checkSessionToken } from '@/assets/js/authentication.js';
import SideNav from '@/components/Navigation/SideNav.vue';
import TopNav from '@/components/Navigation/TopNav.vue';

export default {
  name: 'Admin',
  components: {
    SideNav,
    TopNav,
  },
  data() {
    return {
      email: '',
      fullName: '',
      isAdmin: false,
      selected: 'course',
    };
  },
  async created() {
    await checkSessionToken().then(() => {
      this.email = window.sessionStorage.getItem('learner_email');
      this.fullName = window.sessionStorage.getItem('learner_fullname');
      this.isAdmin = window.sessionStorage.getItem('learner_isAdmin') == 'true';
    });
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/styles/shared';

.content-body {
  padding-top: 1.5em;

  li {
    padding: 4px 0;
  }
}
</style>
