<template>
  <div class="profile-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-4 col-lg-3 mb-4">
          <!-- EmailOption component to give user choice of opting in or out of email reminders -->
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h2 class="profile-title text-black">Email Reminders</h2>
            </div>
            <div>
              <EmailOption class="form-control" />
            </div>
          </div>
        </div>
        <div class="col-md-8 col-lg-9 mb-4">
          <!-- Events component to display upcoming reminders -->
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h2 class="profile-title text-black">Upcoming Events</h2>
            </div>
            <div class="card-body">
              <Events
                :vehicles="vehicles"
                @update-vehicles="handleUpdateVehicles"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import Events from "@/components/Events.vue";
import EmailOption from "@/components/EmailOption.vue";

interface Vehicle {
  id: number;
  make: string;
  colour: string;
  registrationNumber: string;
  yearOfManufacture: number;
  fuelType: string;
  engineCapacity: number;
  taxStatus: string;
  taxDueDate: string;
  motStatus: string;
  motExpiryDate: string;
}

export default defineComponent({
  components: {
    Events,
    EmailOption,
  },
  setup() {
    const addedVehicles = ref<Vehicle[]>([]);

    const addVehicle = (vehicle: Vehicle) => {
      addedVehicles.value.push(vehicle);
    };

    return {
      addedVehicles,
      addVehicle,
    };
  },
  data() {
    return {
      vehicles: [] as Vehicle[],
    };
  },
  methods: {
    handleUpdateVehicles(data: Vehicle[]) {
      this.vehicles = data;
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
