<template>
  <div class="add-log">
    <div class="card-body">
      <form @submit.prevent="submitPost">
        <div class="form-group">
          <label class="form-label" for="title">Title</label>
          <input
            name="title"
            type="text"
            class="form-control mb-3"
            v-model="title"
            required
            maxlength="100"
          />
        </div>
        <div class="form-group">
          <label class="form-label" for="description">Description</label>
          <textarea
            name="description"
            class="form-control mb-3"
            rows="8"
            v-model="description"
            required
            maxlength="5000"
          ></textarea>
        </div>
        <div class="form-group text-center">
          <label
            class="image-upload-label"
            :class="{ 'image-selected': image_upload }"
          >
            <input
              name="upload"
              type="file"
              class="image-upload-input"
              @change="handleImageChange"
              accept=".jpg,.jpeg,.png"
            />
            <i class="fas fa-cloud-upload-alt"></i>
            <span
              class="image-upload-text"
              :class="{ 'image-selected': image_upload }"
              >{{ image_upload ? image_upload.name : "Choose an image" }}</span
            >
          </label>
        </div>
        <button type="submit" class="btn btn-gradient btn-lg btn-block">
          Submit
        </button>
      </form>
      <div v-if="loading" class="loading">Submitting...</div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  data() {
    return {
      title: "",
      description: "",
      image_upload: null,
      loading: false,
      error: "",
    };
  },
  methods: {
    handleImageChange(event: any) {
      const image = event.target.files[0];
      const allowedExtensions = ["jpg", "jpeg", "png"];
      const extension = image.name.split(".").pop().toLowerCase();

      if (!allowedExtensions.includes(extension)) {
        alert("Only .jpg, .jpeg, or .png files are allowed.");
        event.target.value = "";
        this.image_upload = null;
        return;
      }

      this.image_upload = image;
    },
    async submitPost() {
      this.loading = true;

      const formData = new FormData();
      formData.append("title", this.title);
      formData.append("description", this.description);

      if (this.image_upload) {
        formData.append("image_upload", this.image_upload);
      }

      try {
        console.log(this.vehicleId);
        console.log(formData);

        const response = await fetch(`http://localhost:8000/add-post/`, {
          method: "POST",
          credentials: "include",
          body: formData,
        });

        if (response.ok) {
          console.log(response);
          window.location.reload();
        } else {
          console.error(
            "Failed to submit post:",
            response.status,
            response.statusText
          );
        }

        this.title = "";
        this.description = "";
        this.image_upload = null;
        this.loading = false;
        this.error = "";
      } catch (error) {
        console.error("Error submitting post:", error);
        this.loading = false;
        this.error = "Failed to submit post. Please try again later.";
      }
    },
  },
  props: {
    vehicleId: {
      type: String,
      required: true,
    },
  },
});
</script>

<style scoped>
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
