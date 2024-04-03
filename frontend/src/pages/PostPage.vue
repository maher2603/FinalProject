<template>
  <div class="profile-page">
    <div class="container">
      <button @click="backToForum" class="btn btn-back">Back to forum</button>
      <div class="row justify-content-center">
        <div class="col-lg-8 mb-4">
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h2 class="profile-title text-black">
                {{ post.title }}
                <span class="username"> - @{{ post.username }} </span>
                <span class="date"> {{ formattedDate }}</span>
              </h2>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div v-if="post.image_upload">
                  <img
                    :src="`http://localhost:8000/${post.image_upload}`"
                    class="post-image"
                  />
                </div>
                <div class="post-description">
                  {{ post.description }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4 mb-4">
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h2 class="profile-title text-black">Comments</h2>
            </div>
            <div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useRoute } from "vue-router";

interface Post {
  id: number;
  user_id: string;
  username: string;
  title: string;
  description: string;
  date_posted: string;
  image_upload: string;
}

export default defineComponent({
  components: {},
  data() {
    return {
      post: {} as Post,
    };
  },
  setup() {
    const route = useRoute();
    const postId = computed(() => {
      const param = route.params.postId;
      if (Array.isArray(param)) {
        return param[0];
      }
      return param;
    });

    return { postId };
  },
  computed: {
    formattedDate(): string {
      if (!this.post.date_posted) return "";
      const date = new Date(this.post.date_posted);
      return date.toLocaleString();
    },
  },
  mounted() {
    this.getPost();
  },
  methods: {
    async getPost() {
      try {
        const response = await fetch(
          `http://localhost:8000/get-post/${this.postId}/`,
          {
            method: "GET",
            credentials: "include",
          }
        );
        if (response.ok) {
          // Parse response data as JSON
          const data = await response.json();
          this.post = data;
          console.log(this.post);
        } else {
          console.error(
            "Failed to fetch vehicles data:",
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error during fetch:", error);
      }
    },
    backToForum() {
      this.$router.push({ name: "Forum Page" });
    },
  },
  props: {
    postId: {
      type: String,
      required: true,
    },
  },
});
</script>

<style scoped>
.username {
  font-size: medium;
  color: rgb(107, 107, 107);
}

.date {
  font-size: medium;
  color: rgb(107, 107, 107);
  padding-top: 40px;
  padding-left: 40px;
  float: right;
}

.profile-page {
  padding-top: 10px;
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

.btn-back {
  padding-left: 20px;
  text-decoration: underline;
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

.post-image {
  width: 100%;
  object-fit: cover;
}

.post-description {
  padding: 20px;
}
</style>
