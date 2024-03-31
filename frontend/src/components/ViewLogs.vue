<template>
  <div class="vehicle-list">
    <div v-if="logs.length > 0">
      <p class="total-cost">Total Spent: £{{ totalCost }}</p>
      <div v-for="log in logs" :key="log.id" class="vehicle-item">
        <div class="vehicle-details">
          <div class="vehicle-info">
            <span class="info-label">Title:</span> {{ log.title }}
          </div>
          <div class="vehicle-info">
            <span class="info-label">Date:</span> {{ log.date }}
          </div>
          <div class="vehicle-info">
            <span class="info-label">Cost: £</span> {{ log.cost }}
          </div>
          <div class="vehicle-info">
            <span class="info-label">Description:</span> {{ log.description }}
          </div>
        </div>
        <button @click="deleteLog(log.id)" class="btn-remove">Delete</button>
      </div>
    </div>
    <div v-else>
      <p class="start-text">Add a log to get started</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

interface Log {
  id: number;
  title: string;
  date: string;
  cost: number;
  description: string;
}

export default defineComponent({
  data() {
    return {
      logs: [] as Log[],
      loading: false,
    };
  },
  computed: {
    totalCost(): number {
      return this.logs.reduce(
        (total, log) => total + parseFloat(String(log.cost)),
        0
      );
    },
  },
  async mounted() {
    await this.fetchLogs();
  },
  methods: {
    async fetchLogs() {
      this.loading = true;
      try {
        const response = await fetch(
          `http://localhost:8000/get-vehicle-logs/${this.vehicleId}/`,
          {
            method: "GET",
            credentials: "include",
          }
        );
        if (response.ok) {
          const logs = await response.json(); // Parse the response JSON data
          this.logs = logs;
          console.log(this.logs);
        } else {
          console.error(
            "Failed to fetch logs:",
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error fetching logs:", error);
      } finally {
        this.loading = false;
      }
    },
    async deleteLog(logId: number) {
      if (confirm("Are you sure you want to delete this log?")) {
        try {
          const response = await fetch(
            `http://localhost:8000/delete-vehicle-log/${logId}/`,
            {
              method: "DELETE",
              credentials: "include",
            }
          );
          if (response.ok) {
            // Remove the deleted log from the UI
            this.logs = this.logs.filter((log) => log.id !== logId);
          } else {
            console.error(
              "Failed to delete log:",
              response.status,
              response.statusText
            );
          }
        } catch (error) {
          console.error("Error deleting log:", error);
        }
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
  padding-right: 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-logs {
  background-color: #060606;
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

.btn-logs:hover {
  background-color: #707070;
}

.start-text {
  color: #c60000;
  padding: 30px;
  font-weight: bold;
  text-align: center;
}

.total-cost {
  text-align: left;
  padding-left: 20px;
  font-weight: bold;
}
</style>
