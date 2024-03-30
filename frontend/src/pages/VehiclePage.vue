<template>
  <div class="profile-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-4 col-lg-3 mb-4">
          <!-- VehicleSearch component to add vehicles by searching DVLA database -->
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h2 class="profile-title text-black">Add Vehicle</h2>
            </div>
            <div>
              <VehicleSearch class="form-control" @vehicle-added="addVehicle" />
            </div>
          </div>
        </div>
        <div class="col-md-8 col-lg-9 mb-4">
          <!-- VehicleList component to display added vehicles -->
          <div class="profile-container">
            <div class="profile-header bg-gradient rounded-top">
              <h2 class="profile-title text-black">My Vehicles</h2>
            </div>
            <div class="card-body">
              <VehicleList
                :vehicles="vehicles"
                @update-vehicles="handleUpdateVehicles"
                @view-logs="viewLogs"
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
import { useRouter } from "vue-router";
import VehicleList from "@/components/VehicleList.vue";
import VehicleSearch from "@/components/VehicleSearch.vue";

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
    VehicleList,
    VehicleSearch,
  },
  setup() {
    const addedVehicles = ref<Vehicle[]>([]);
    const vehicleId = ref<number>(0);

    const router = useRouter();

    const viewLogs = (id: number) => {
      vehicleId.value = id;
      console.log({ vehicleId: id });
      router.push({ name: "Log Page", params: { vehicleId: id } });
    };

    const addVehicle = (vehicle: Vehicle) => {
      addedVehicles.value.push(vehicle);
    };

    return {
      addedVehicles,
      addVehicle,
      viewLogs,
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
