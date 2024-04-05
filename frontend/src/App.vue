<template>
  <div class="bg-light d-flex flex-column" style="min-height: 100vh">
    <!-- Header -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-theme">
      <div class="container">
        <!-- Navbar brand -->
        <router-link
          class="nav-link navbar-brand fw-bold"
          style="font-size: x-large"
          :to="{ name: 'Main Page' }"
          >Whips & Gigs</router-link
        >

        <!-- Navbar toggler -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Navbar links -->
        <div
          class="collapse navbar-collapse justify-content-end"
          id="navbarNav"
        >
          <ul class="navbar-nav">
            <!-- Forum Page link -->
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Forum Page' }"
                >Forum</router-link
              >
            </li>
            <!-- Vehicle Page link -->
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Vehicle Page' }"
                >Garage</router-link
              >
            </li>
            <!-- Profile Page link -->
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'Profile Page' }"
                >Profile</router-link
              >
            </li>
            <!-- Logout button -->
            <li class="nav-item">
              <button type="button" class="nav-link" @click="logout">
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main content area -->
    <main class="container-fluid flex-grow-1 p-0">
      <router-view v-slot="{ Component }">
        <transition name="slide" mode="out-in">
          <component :is="Component"></component>
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script lang="js">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
  components: { RouterView },

  methods: {
    async logout() {
      window.location.href = "http://localhost:8000/logout/";
    },
  },
});
</script>

<style scoped>
.bg-theme {
  background-color: hsl(0, 0%, 8%);
}

.slide-enter-active,
.slide-leave-active {
  transition: opacity 1s, transform 1s;
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(-100%);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(100%);
}
</style>
