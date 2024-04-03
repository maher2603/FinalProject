<template>
  <div class="vehicle-list">
    <div v-if="posts.length > 0">
      <div v-for="post in posts" :key="post.id" class="post-item">
        <div class="post-title">
          {{ post.title }} <span class="username"> - @{{ post.username }}</span>
          <button
            v-if="post.user_id === userId"
            @click="deletePost(post.id)"
            class="btn btn-remove"
          >
            Delete
          </button>
        </div>
        <div class="mb-3">
          <div v-if="post.image_upload" class="mt-2">
            <img :src="post.image_upload" class="post-image" />
          </div>
        </div>
        <div class="post-description">
          {{ post.description }}
        </div>
        <button class="btn btn-logs" @click="viewPost(post.id)">
          View Post
        </button>
      </div>
    </div>
    <div v-else>
      <p class="start-text">There are no posts available at the moment</p>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";

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
  data() {
    return {
      posts: [] as Post[],
      loading: false,
    };
  },
  async mounted() {
    await this.fetchPosts();
  },
  methods: {
    async fetchPosts() {
      this.loading = true;
      try {
        const response = await fetch(`http://localhost:8000/get-posts/`, {
          method: "GET",
          credentials: "include",
        });
        if (response.ok) {
          const posts = await response.json();
          this.posts = posts
            .map((post: Post) => ({
              ...post,
              image_upload: post.image_upload
                ? `http://localhost:8000/${post.image_upload}`
                : null,
            }))
            .sort((a, b) => {
              return (
                new Date(b.date_posted).getTime() -
                new Date(a.date_posted).getTime()
              );
            });
        } else {
          console.error(
            "Failed to fetch logs:",
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error fetching logs:", error);
      } finally {
        this.loading = false;
      }
    },
    async deletePost(postId: number) {
      if (confirm("Are you sure you want to delete this post?")) {
        try {
          const response = await fetch(
            `http://localhost:8000/delete-post/${postId}/`,
            {
              method: "DELETE",
              credentials: "include",
            }
          );
          if (response.ok) {
            // Remove the deleted post from the UI
            this.posts = this.posts.filter((post) => post.id !== postId);
          } else {
            console.error(
              "Failed to delete post:",
              response.status,
              response.statusText
            );
          }
        } catch (error) {
          console.error("Error deleting post:", error);
        }
      }
    },
    async viewPost(postId: number) {
      this.$emit("view-post", postId);
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
.post-title {
  font-size: larger;
  font-weight: Bold;
  padding-bottom: 10px;
}

.post-description {
  padding: 20px;
  padding-bottom: 0px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.post-item {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.username {
  font-size: medium;
  color: rgb(107, 107, 107);
}

.btn {
  padding: 0px;
  padding-right: 20px;
  border: none;
}

.btn-logs {
  text-decoration: underline;
}

.btn-remove {
  background-color: #c60000;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  float: right;
}

.btn-remove:hover {
  background-color: #ff0000;
}

.start-text {
  color: #c60000;
  padding: 30px;
  font-weight: bold;
  text-align: center;
}

.post-image {
  width: 100%;
  height: 250px;
  object-fit: cover;
}
</style>
