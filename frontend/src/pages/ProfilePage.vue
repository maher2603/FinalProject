<template>
  <div class="profile-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h1 class="profile-title text-black">
                Welcome, {{ user.username }}
              </h1>
            </div>
            <div class="profile-body bg-light rounded-bottom">
              <div v-if="user">
                <form @submit.prevent="updateProfile" class="profile-form">
                  <div class="mb-3">
                    <label for="email" class="form-label">Email Address:</label>
                    <input
                      v-model="user.email"
                      id="email"
                      class="form-control"
                      required
                    />
                  </div>
                  <div class="mb-3">
                    <label for="username" class="form-label">Username:</label>
                    <input
                      v-model="user.username"
                      id="username"
                      class="form-control"
                      required
                    />
                  </div>
                  <div class="mb-3">
                    <label for="dob" class="form-label">Date of Birth:</label>
                    <input
                      v-model="user.dob"
                      id="dob"
                      class="form-control"
                      type="date"
                      required
                    />
                  </div>
                  <div class="mb-3">
                    <div v-if="user.profileImage" class="mt-2">
                      <img
                        :src="user.profileImage"
                        width="150"
                        height="150"
                        class="profile-image rounded-circle"
                      />
                    </div>
                  </div>
                  <button
                    type="submit"
                    class="btn btn-gradient btn-lg btn-block"
                  >
                    Update Profile
                  </button>
                </form>
              </div>
              <div v-else>
                <p>Loading...</p>
              </div>
              <div class="error" v-if="error">
                <p>{{ error }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

interface UserData {
  id: number | null;
  username: string;
  email: string;
  dob: string;
  profileImage: string | null;
}

export default defineComponent({
  data() {
    return {
      user: {
        id: null as number | null,
        username: "",
        email: "",
        dob: "",
        profileImage: null as string | null,
      } as UserData,
      error: "",
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
          console.error(
            "Failed to fetch user data:",
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error during fetch:", error);
      }
    },

    async updateProfile() {
      const profileData = {
        email: this.user.email,
        dob: this.user.dob,
        username: this.user.username,
      };

      try {
        const response = await fetch(
          "http://localhost:8000/update_user_profile/",
          {
            method: "PUT",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(profileData),
          }
        );

        if (response.ok) {
          if (this.user.profileImage != "") {
            console.log("The profile updated successfully");
            console.log(this.user);
            this.fetchUserProfile();
            this.error = "Profile updated successfully";
          } else {
            console.log("The profile updated successfully");
            console.log(this.user);
            this.fetchUserProfile();
            this.error = "Profile updated successfully";
          }
        } else {
          console.error(
            "Failed to update user profile:",
            response.status,
            response.statusText
          );
          this.error = "Failed to update user profile";
        }
      } catch (error) {
        console.error("There was an error while updating the profile:", error);
        this.error = "Failed to update user profile";
      }
    },
  },
});
</script>

<style scoped>
.profile-page {
  padding-top: 50px;
  padding-bottom: 50px;
}

.profile-container {
  background-color: #f9f9f9;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.profile-header {
  padding: 20px;
  text-align: center;
}

.profile-title {
  font-size: 32px;
  font-weight: bold;
}

.profile-body {
  padding: 20px;
}

.profile-image {
  border: 5px solid #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.btn-block {
  border-radius: 25px;
}

.btn-gradient {
  background: linear-gradient(to right, #ff416c, #ff4b2b);
  color: #fff;
}

.bg-gradient {
  background: linear-gradient(to right, #ff416c, #ff4b2b);
  color: #fff;
}

.error {
  padding-top: 20px;
  color: red;
  font-weight: bold;
}
</style>
