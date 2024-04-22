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
                  class="btn btn-remove"
                  @click="deleteComment(comment.id)"
                >
                  Delete
                </button></span
              >{{ formattedDate(comment.date_posted) }}</span
            >
            <span>
              <button
                @click="toggleReplyForm(comment.id)"
                class="btn btn-reply"
              >
                {{ showReplyForm[comment.id] ? "Cancel" : "Reply" }}
              </button>
            </span>
            <div v-if="showReplyForm[comment.id]">
              <form @submit.prevent="addReply(comment.id)">
                <div class="input-group">
                  <textarea
                    v-model="newReply"
                    class="form-control"
                    rows="1"
                    placeholder="Your reply"
                  ></textarea>
                  <button type="submit" class="btn btn-gradient">Submit</button>
                </div>
              </form>
            </div>
            <div
              v-for="reply in replies[comment.id]"
              :key="reply.id"
              class="reply-item"
            >
              <div class="comment">
                <span class="username">{{ reply.username }}</span>
                :
                {{ reply.reply }}
                <span class="date"
                  ><span v-if="reply.user_id == user.id">
                    <button
                      class="btn btn-remove"
                      @click="deleteReply(reply.id)"
                    >
                      Delete
                    </button></span
                  >{{ formattedDate(reply.date_posted) }}</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";

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

interface Reply {
  id: number;
  comment_id: string;
  user_id: string;
  username: string;
  post_id: string;
  reply: string;
  date_posted: string;
}

export default defineComponent({
  setup() {
    const showReplyForm = reactive({} as Record<number, boolean>);
    const replyText = reactive("");

    const toggleReplyForm = (commentId: number) => {
      showReplyForm[commentId] = !showReplyForm[commentId];
    };
    return {
      showReplyForm,
      replyText,
      toggleReplyForm,
    };
  },
  data() {
    return {
      comments: {} as Comment,
      newComment: "",
      user: {} as UserData,
      replies: {} as Reply,
      newReply: "",
    };
  },
  mounted() {
    this.getComments().then(() => {
      for (const comment of this.comments) {
        this.getReplies(comment.id);
      }
    });
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
    async addReply(commentId) {
      try {
        const response = await fetch(
          `http://localhost:8000/add-reply/${commentId}/`,
          {
            method: "POST",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ reply: this.newReply }),
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
    async getReplies(commentId) {
      try {
        const response = await fetch(
          `http://localhost:8000/get-replies/${commentId}/`,
          {
            method: "GET",
            credentials: "include",
          }
        );
        if (response.ok) {
          const data = await response.json();
          // console.log("Replies fetched:", data);
          const comment = this.comments.find(
            (comment) => comment.id === commentId
          );
          if (comment) {
            this.replies[commentId] = data;
          }
          // console.log(this.replies[commentId]);
        } else {
          console.error(
            "Failed to fetch replies:",
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error during fetch:", error);
      }
    },
    async deleteReply(replyId: number) {
      if (confirm("Are you sure you want to delete this comment?")) {
        try {
          const response = await fetch(
            `http://localhost:8000/delete-reply/${replyId}/`,
            {
              method: "DELETE",
              credentials: "include",
            }
          );
          if (response.ok) {
            window.location.reload();
          } else {
            console.error(
              "Failed to delete reply:",
              response.status,
              response.statusText
            );
          }
        } catch (error) {
          console.error("Error deleting reply:", error);
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

.reply-item {
  padding-top: 10px;
  padding-left: 20px;
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
  padding-left: 0px;
}
</style>
