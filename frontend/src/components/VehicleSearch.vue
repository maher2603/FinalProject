<template>
  <div>
    <label class="form-label" for="registrationNumber"
      >Registration Number:</label
    >
    <input
      class="form-control mb-3"
      type="text"
      id="registrationNumber"
      v-model="registrationNumber"
    />
    <button class="btn btn-gradient btn-lg btn-block" @click="searchVehicle">
      Search
    </button>
    <div class="loading" v-if="loading">
      <p>Loading...</p>
    </div>
    <div class="search-result" v-if="searchResult">
      <h3>Search Result</h3>
      <p>
        <strong>Registration Number:</strong>
        {{ searchResult.registrationNumber }}
      </p>
      <p><strong>Make:</strong> {{ searchResult.make }}</p>
      <p><strong>Colour:</strong> {{ searchResult.colour }}</p>
      <p>
        <strong>Year of Manufacture:</strong>
        {{ searchResult.yearOfManufacture }}
      </p>
      <p><strong>Fuel Type:</strong> {{ searchResult.fuelType }}</p>
      <p>
        <strong>Engine Capacity:</strong> {{ searchResult.engineCapacity }}cc
      </p>
      <p>
        <strong>Tax Status:</strong> {{ searchResult.taxStatus }} until
        {{ searchResult.taxDueDate }}
      </p>
      <p>
        <strong>MOT Status:</strong> {{ searchResult.motStatus }} until
        {{ searchResult.motExpiryDate }}
      </p>
      <button class="btn btn-gradient btn-lg btn-block" @click="addVehicle">
        Add Vehicle
      </button>
    </div>
    <div class="error" v-if="error">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import axios from "axios";

interface UserData {
  id: number | null;
  username: string;
  email: string;
  dob: string;
  profileImage: string | null;
}

interface SearchResult {
  registrationNumber: string;
  make: string;
  colour: string;
  yearOfManufacture: number;
  fuelType: string;
  engineCapacity: number;
  taxStatus: string;
  taxDueDate: string;
  motStatus: string;
  motExpiryDate: string;
}

export default {
  data() {
    return {
      user: {
        id: null as number | null,
        username: "",
        email: "",
        dob: "",
        profileImage: null as string | null,
      } as UserData,
      registrationNumber: "",
      loading: false,
      error: "",
      searchResult: null as SearchResult | null,
    };
  },
  methods: {
    async searchVehicle() {
      this.loading = true;
      try {
        const url = "http://localhost:8000/vehicle-search/";
        const data = JSON.stringify({
          registrationNumber: this.registrationNumber,
        });
        const response = await axios.post(url, data, {
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.status === 200) {
          this.searchResult = response.data;
          this.error = "";
        } else {
          this.error = "Failed to fetch vehicle data";
        }
      } catch (error) {
        this.error = "Vehicle not found";
        console.error("Error while fetching vehicle data:", error);
      } finally {
        this.loading = false;
      }
    },
    async addVehicle() {
      if (this.searchResult) {
        const data = {
          registration_number: this.searchResult.registrationNumber,
          make: this.searchResult.make,
          colour: this.searchResult.colour,
          year_of_manufacture: this.searchResult.yearOfManufacture,
          fuel_type: this.searchResult.fuelType,
          engine_capacity: this.searchResult.engineCapacity,
          tax_status: this.searchResult.taxStatus,
          tax_due_date: this.searchResult.taxDueDate,
          mot_status: this.searchResult.motStatus,
          mot_expiry_date: this.searchResult.motExpiryDate,
        };

        try {
          const response = await axios.post(
            "http://localhost:8000/add-vehicle/",
            data,
            { withCredentials: true }
          );
          console.log("Vehicle added successfully:", response.data);
          this.$emit("vehicle-added", this.searchResult);
          this.registrationNumber = "";
          this.searchResult = null;
          window.location.reload();
        } catch (error) {
          this.error = "Failed to add vehicle";
        }
      } else {
        console.error("searchResult is null");
      }
    },

    showVehicle() {
      this.$emit("vehicle-added", this.searchResult);
      this.registrationNumber = "";
      this.searchResult = null;
    },
  },
};
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
</style>
