<template>
  <div class="profile-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-4 col-lg-3 mb-4">
          <!-- AddLog component to manually add logs to vehicle-->
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h2 class="profile-title text-black">Add Log</h2>
            </div>
            <div>
              <!-- Pass the vehicleId as a prop to AddLog component -->
              <AddLog class="form-control" :vehicleId="vehicleId" />
            </div>
          </div>
        </div>
        <div class="col-md-8 col-lg-9 mb-4">
          <!-- ViewLogs component to view all logs for vehicle -->
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h2 class="profile-title text-black">Vehicle Logs</h2>
            </div>
            <div class="card-body">
              <!-- Pass the vehicleId as a prop to ViewLogs component -->
              <ViewLogs :vehicleId="vehicleId" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useRoute } from "vue-router";
import ViewLogs from "@/components/ViewLogs.vue";
import AddLog from "@/components/AddLog.vue";

export default defineComponent({
  components: {
    ViewLogs,
    AddLog,
  },
  setup() {
    const route = useRoute();
    const vehicleId = computed(() => {
      const param = route.params.vehicleId;
      if (Array.isArray(param)) {
        return param[0];
      }
      return param;
    });

    return { vehicleId };
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
