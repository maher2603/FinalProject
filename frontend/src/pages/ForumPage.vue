<template>
  <div class="profile-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-4 col-lg-3 mb-4">
          <!-- AddPost component to allow user to add forum post -->
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h2 class="profile-title text-black">Add Post</h2>
            </div>
            <div>
              <AddPost class="form-control" />
            </div>
          </div>
        </div>
        <div class="col-md-8 col-lg-9 mb-4">
          <!-- ViewPosts component to display all forum posts -->
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h2 class="profile-title text-black">Forum</h2>
            </div>
            <div class="card-body">
              <ViewPosts :userId="user.id" @view-post="viewPost" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import ViewPosts from "@/components/ViewPosts.vue";
import AddPost from "@/components/AddPost.vue";

interface UserData {
  id: string | null;
  username: string;
  email: string;
  dob: string;
  profileImage: string | null;
}

export default defineComponent({
  components: {
    ViewPosts,
    AddPost,
  },
  setup() {
    const postId = ref<number>(0);

    const router = useRouter();

    const viewPost = (id: number) => {
      postId.value = id;
      console.log({ postId: id });
      router.push({ name: "Post Page", params: { postId: id } });
    };

    return {
      viewPost,
    };
  },
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
  props: {
    userId: {
      type: String,
      required: true,
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

.form-control {
  border-radius: 10px;
  padding: 20px;
  border: 0px;
  background-color: #f9f9f900;
}
</style>
