<template>
  <div class="add-log">
    <div class="card-body">
      <form @submit.prevent="addComment">
        <div class="input-group">
          <textarea
            v-model="newComment"
            class="form-control"
            rows="1"
            placeholder="Enter your comment"
          ></textarea>
          <button type="submit" class="btn btn-gradient">Submit</button>
        </div>
      </form>
      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment">
            <span class="username">{{ comment.username }}</span> :
            {{ comment.comment }}
            <span class="date"
              ><span v-if="comment.user_id.id === user.id">
                <button
                  @click="deleteComment(comment.id)"
                  class="btn btn-remove"
                >
                  Delete
                </button> </span
              >{{ formattedDate(comment.date_posted) }}</span
            >
            <span><button class="btn btn-reply">Reply</button></span>
          </div>
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

interface Comment {
  id: number;
  user_id: string;
  username: string;
  post_id: string;
  comment: string;
  date_posted: string;
}

export default defineComponent({
  data() {
    return {
      comments: {} as Comment,
      newComment: "",
      user: {} as UserData,
    };
  },
  mounted() {
    this.getComments();
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

    formattedDate(date_posted: string): string {
      if (!date_posted) return "";
      const date = new Date(date_posted);
      return date.toLocaleString();
    },
    async addComment() {
      try {
        const response = await fetch(
          `http://localhost:8000/add-comment/${this.postId}/`,
          {
            method: "POST",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ comment: this.newComment }),
          }
        );
        if (response.ok) {
          this.newComment = "";
          window.location.reload();
        } else {
          console.error(
            "Failed to add comment:",
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error adding comment:", error);
      }
    },
    async getComments() {
      try {
        const response = await fetch(
          `http://localhost:8000/get-comments/${this.postId}/`,
          {
            method: "GET",
            credentials: "include",
          }
        );
        if (response.ok) {
          // Parse response data as JSON
          const data = await response.json();
          this.comments = data;
          console.log(this.post);
        } else {
          console.error(
            "Failed to fetch comments:",
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error during fetch:", error);
      }
    },
    async deleteComment(commentId: number) {
      if (confirm("Are you sure you want to delete this comment?")) {
        try {
          const response = await fetch(
            `http://localhost:8000/delete-comment/${commentId}/`,
            {
              method: "DELETE",
              credentials: "include",
            }
          );
          if (response.ok) {
            // window.location.reload();
            this.comments = this.comments.filter(
              (comment) => comment.id !== commentId
            );
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
.comments-list {
  padding: 10px;
}

.comment-item {
  padding-bottom: 10px;
}

.error {
  padding-top: 20px;
  color: red;
  font-weight: bold;
}

.btn-block {
  border-radius: 25px;
}

.btn-gradient {
  background: linear-gradient(to right, #ff416c, #ff4b2b);
  color: #fff;
}

.btn-reply {
  text-decoration: underline;
  font-size: small;
  padding-top: 0px;
  padding-right: 5px;
}

.comment {
  padding-bottom: 0px;
}

.bg-gradient {
  background: linear-gradient(to right, #ff416c, #ff4b2b);
  color: #fff;
}

.search-result {
  padding-top: 20px;
}

.loading {
  padding-top: 30px;
  color: #c60000;
  font-weight: bold;
}

.image-upload-label {
  display: inline-block;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  border-radius: 10px;
  padding: 10px 20px;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.image-upload-label:hover {
  background-color: #f0f0f0;
}

.image-upload-label.image-selected {
  background-color: hsl(0, 0%, 8%);
}

.image-upload-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.image-upload-text.image-selected {
  color: white;
}

.username {
  font-size: medium;
  font-weight: bold;
  color: rgb(107, 107, 107);
}

.date {
  font-size: x-small;
  color: rgb(107, 107, 107);
  float: right;
}

.btn-remove {
  color: #c60000;
  font-size: small;
  padding-top: 0px;
  padding-left: 0px;
}
</style>
