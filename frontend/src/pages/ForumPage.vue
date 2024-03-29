<template>
  <div class="home-page">
    <div class="container">
      <div class="card">
        <div class="card-header bg-dark text-white">
          <h1 class="card-title">Forum</h1>
        </div>
        <div class="card-body">
          <p class="card-text">Chat to some pussios</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

interface UserData {
  id: string | null;
  username: string;
  email: string;
  dob: string;
  profileImage: string | null;
}

export default defineComponent({
  data() {
    return {
      user: {
        id: null as string | null,
        username: "",
        email: "",
        dob: "",
        profileImage: null as string | null,
      } as UserData,
    };
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await fetch("http://localhost:8000/user-api/", {
          method: "GET",
          credentials: "include",
        });

        if (response.ok) {
          const userData = (await response.json()) as UserData;
          this.user = userData;
          if (userData.profileImage) {
            userData.profileImage = `http://localhost:8000/${userData.profileImage}`;
          }
        } else {
          console.error("Failed to fetch user data");
        }
      } catch (error) {
        console.error("There was an error during fetch:", error);
      }
    },
  },
});
</script>

<style scoped>
.home-page {
  padding-top: 5px;
}

.profile-info {
  margin-top: 20px;
}

.profile-details {
  display: flex;
  align-items: center;
}

.profile-image {
  margin-right: 20px;
  width: 100px;
  height: 100px;
}

.profile-text {
  flex-grow: 1;
}
</style>
