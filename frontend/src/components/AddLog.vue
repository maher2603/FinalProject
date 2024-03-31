<template>
  <div class="add-log">
    <div class="card-body">
      <form @submit.prevent="submitLog">
        <div class="form-group">
          <label class="form-label" for="title">Title</label>
          <input
            name="title"
            type="text"
            class="form-control mb-3"
            v-model="title"
            required
          />
        </div>
        <div class="form-group">
          <label class="form-label" for="date">Date</label>
          <input
            name="date"
            type="date"
            class="form-control mb-3"
            v-model="date"
            required
          />
        </div>
        <div class="form-group">
          <label class="form-label" for="cost">Cost (£)</label>
          <input
            name="cost"
            type="text"
            class="form-control mb-3"
            v-model="cost"
            required
            pattern="^\d+(\.\d{1,2})?$"
          />
        </div>
        <div class="form-group">
          <label class="form-label" for="description">Description</label>
          <textarea
            name="description"
            class="form-control mb-3"
            rows="4"
            v-model="description"
            required
          ></textarea>
        </div>
        <div class="form-group text-center">
          <label class="file-upload-label" :class="{ 'file-selected': file }">
            <input
              name="upload"
              type="file"
              class="file-upload-input"
              @change="handleFileChange"
            />
            <i class="fas fa-cloud-upload-alt"></i>
            <span class="file-upload-text" :class="{ 'file-selected': file }">{{
              file ? file.name : "Choose a file"
            }}</span>
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
// import axios from "axios";

export default defineComponent({
  data() {
    return {
      title: "",
      date: "",
      cost: "",
      description: "",
      file: null,
      loading: false,
      error: "",
    };
  },
  methods: {
    handleFileChange(event: any) {
      this.file = event.target.files[0];
    },
    async submitLog() {
      this.loading = true;

      const formData = new FormData();
      formData.append("title", this.title);
      formData.append("date", this.date);
      formData.append("cost", this.cost);
      formData.append("description", this.description);

      if (this.file) {
        formData.append("file", this.file);
      }

      try {
        console.log(this.vehicleId);
        console.log(formData);

        const response = await fetch(
          `http://localhost:8000/add-vehicle-log/${this.vehicleId}/`,
          {
            method: "POST",
            credentials: "include",
            body: formData,
          }
        );

        if (response.ok) {
          // Parse response data as JSON
          console.log(response);
          window.location.reload();
        } else {
          console.error(
            "Failed to submit log:",
            response.status,
            response.statusText
          );
        }

        // Reset form fields
        this.title = "";
        this.date = "";
        this.cost = "";
        this.description = "";
        this.file = null;
        this.loading = false;
        this.error = "";
      } catch (error) {
        console.error("Error submitting log:", error);
        this.loading = false;
        this.error = "Failed to submit log. Please try again later.";
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

.file-upload-label {
  display: inline-block;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  border-radius: 10px;
  padding: 10px 20px;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.file-upload-label:hover {
  background-color: #f0f0f0;
}

.file-upload-label.file-selected {
  background-color: hsl(0, 0%, 8%);
}

.file-upload-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.file-upload-text.file-selected {
  color: white;
}
</style>
