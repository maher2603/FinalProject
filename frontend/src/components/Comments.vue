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
          <div>{{ comment.username }} : {{ comment.comment }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

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
    return { comments: {} as Comment, newComment: "" };
  },
  mounted() {
    this.getComments();
  },
  methods: {
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
</style>
