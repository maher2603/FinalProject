// Example of how to use Vue Router

import { createRouter, createWebHistory } from "vue-router";

// 1. Define route components.
import MainPage from "../pages/MainPage.vue";
import ProfilePage from "../pages/ProfilePage.vue";
import VehiclePage from "../pages/VehiclePage.vue";
import LogPage from "../pages/LogPage.vue";
import ForumPage from "../pages/ForumPage.vue";

let base =
  import.meta.env.MODE == "development" ? import.meta.env.BASE_URL : "";

// 2. Define some routes
const router = createRouter({
  history: createWebHistory(base),
  routes: [
    { path: "/", name: "Main Page", component: MainPage },
    { path: "/profile/", name: "Profile Page", component: ProfilePage },
    { path: "/garage/", name: "Vehicle Page", component: VehiclePage },
    { path: "/garage/logs/:vehicleId", name: "Log Page", component: LogPage },
    { path: "/forum/", name: "Forum Page", component: ForumPage },
  ],
});

export default router;
