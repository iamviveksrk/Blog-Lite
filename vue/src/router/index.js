import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/auth",
    name: "auth",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../views/AuthView.vue"),
  },
  {
    path: "/profile/:username",
    name: "profile",
    component: () => import("../views/ProfileView.vue"),
  },
  {
    path : '/post/manage/:post_id?',
    name : 'manage_post',
    component: () => import("../views/PostManageView.vue"),
  },
  {
    path : '/search',
    name : 'search',
    component: () => import("../views/SearchView.vue"),
  },
  {
    path : '/avatar',
    name : 'avatar',
    component: () => import("../views/AvatarView.vue"),
  },
];

const router = new VueRouter({
  // mode : 'history',
  routes,
});

export default router;
