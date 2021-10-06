import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/assigntrainers",
    name: "AssignTrainers",
    component: () =>
      import(
        /* webpackChunkName: "assigntrainers" */ "../views/AssignTrainers.vue"
      ),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
