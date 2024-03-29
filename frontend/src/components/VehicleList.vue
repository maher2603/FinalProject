<template>
  <div class="vehicle-list">
    <div v-if="vehicles.length > 0">
      <div
        v-for="(vehicle, index) in vehicles"
        :key="index"
        class="vehicle-item"
      >
        <div class="vehicle-details">
          <div class="vehicle-info">
            <strong class="info-label">Registration Number: </strong>
            <span class="info-value">{{ vehicle.registration_number }}</span>
          </div>
          <div class="vehicle-info">
            <strong class="info-label">Make: </strong>
            <span class="info-value">{{ vehicle.make }}</span>
          </div>
          <div class="vehicle-info">
            <strong class="info-label">Colour: </strong>
            <span class="info-value">{{ vehicle.colour }}</span>
          </div>
          <div class="vehicle-info">
            <strong class="info-label">Year: </strong>
            <span class="info-value">{{ vehicle.year_of_manufacture }}</span>
          </div>
          <div class="vehicle-info">
            <strong class="info-label">Fuel Type: </strong>
            <span class="info-value">{{ vehicle.fuel_type }}</span>
          </div>
          <div class="vehicle-info">
            <strong class="info-label">Engine Capacity: </strong>
            <span class="info-value">{{ vehicle.engine_capacity }}cc</span>
          </div>
          <div v-if="vehicle.tax_status == 'Taxed'" class="vehicle-info">
            <strong class="info-label">Tax Status: </strong>
            <span class="info-value"
              >{{ vehicle.tax_status }} until {{ vehicle.tax_due_date }}</span
            >
          </div>
          <div v-else-if="vehicle.tax_status == 'SORN'" class="vehicle-info">
            <strong class="info-label">Tax Status: </strong>
            <span class="info-value">{{ vehicle.tax_status }}</span>
          </div>
          <div v-else class="vehicle-info">
            <strong class="info-label">Tax Status: </strong>
            <span class="info-value">{{ vehicle.tax_status }}</span>
          </div>
          <div v-if="vehicle.mot_status == 'Valid'" class="vehicle-info">
            <strong class="info-label">MOT Status: </strong>
            <span class="info-value">
              {{ vehicle.mot_status }} until {{ vehicle.mot_expiry_date }}</span
            >
          </div>
          <div v-else="vehicle.mot_status == 'Not valid'" class="vehicle-info">
            <strong class="info-label">MOT Status: </strong>
            <span class="info-value">Expired </span>
          </div>
        </div>
        <button class="btn-remove" @click="removeVehicle(index)">Remove</button>
      </div>
    </div>
    <div v-else>
      <p class="start-text">Add a vehicle to get started</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

interface Vehicle {
  id: number;
  registration_number: string;
  make: string;
  colour: string;
  year_of_manufacture: number;
  fuel_type: string;
  engine_capacity: number;
  tax_status: string;
  tax_due_date: string;
  mot_status: string;
  mot_expiry_date: string;
}

export default defineComponent({
  props: {
    vehicles: {
      type: Array as PropType<Vehicle[]>,
      required: true,
    },
  },
  mounted() {
    // Call getVehicles method when the component is mounted
    this.getVehicles();
  },
  methods: {
    async getVehicles() {
      try {
        // Fetch vehicles data from the backend API
        const response = await fetch("http://localhost:8000/get-vehicles/", {
          method: "GET",
          credentials: "include",
        });
        if (response.ok) {
          // Parse response data as JSON
          const data = await response.json();
          // Emit a custom event to pass the fetched vehicles data to the parent component
          this.$emit("update-vehicles", data);
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
    removeVehicle(index: number) {
      const vehicleToRemove = this.vehicles[index];

      // Send a DELETE request to the backend API to remove the vehicle
      fetch(`http://localhost:8000/remove-vehicle/${vehicleToRemove.id}/`, {
        method: "DELETE",
        credentials: "include",
      })
        .then((response) => {
          if (response.ok) {
            // If the request is successful, emit an event to notify the parent component
            this.$emit("vehicle-removed", index);
            // Reload the page
            window.location.reload();
          } else {
            console.error(
              "Failed to remove vehicle:",
              response.status,
              response.statusText
            );
          }
        })
        .catch((error) => {
          console.error("Error during remove vehicle request:", error);
        });
    },
  },
});
</script>

<style scoped>
.vehicle-list {
  font-family: "Roboto", sans-serif;
}

.vehicle-item {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.vehicle-details {
  display: flex;
  flex-wrap: wrap;
}

.vehicle-info {
  flex: 1 1 50%;
  margin-bottom: 10px;
}

.info-label {
  font-weight: bold;
}

.btn-remove {
  background-color: #c60000;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-remove:hover {
  background-color: #ff0000;
}

.start-text {
  color: #c60000;
  padding: 20px;
  font-weight: bold;
  text-align: center;
}
</style>
