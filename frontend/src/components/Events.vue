<template>
  <div class="event-list">
    <!-- Display events sorted by date -->
    <div v-if="sortedEvents.length > 0">
      <div v-for="event in sortedEvents" :key="event.id" class="event-item">
        <div class="event-details">
          <div class="event-info">
            <span class="info-label">
              {{ event.registration_number }}
              <span
                v-if="event.tax_due_date !== null && event.tax_due_date !== ''"
              >
                <div v-if="event.tax_status !== 'SORN'">
                  <span class="valid" v-if="event.remainingDays >= 0">
                    <span v-if="event.eventType === 'Tax Due'">
                      Tax is due in {{ event.remainingDays }} days ({{
                        event.date
                      }})
                    </span>
                    <span v-else-if="event.eventType === 'MOT Expiry'">
                      MOT expires in {{ event.remainingDays }} days ({{
                        event.date
                      }})
                    </span>
                  </span>
                  <span class="expired" v-else>
                    <span v-if="event.eventType === 'Tax Due'">
                      Tax was due {{ -event.remainingDays }} days ago
                    </span>
                    <span v-else-if="event.eventType === 'MOT Expiry'">
                      MOT expired {{ -event.remainingDays }} days ago
                    </span>
                  </span>
                </div>
              </span>
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Display message if no upcoming events -->
    <p v-else class="start-text">No upcoming events found.</p>
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
  tax_due_date: string | null;
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
  computed: {
    sortedEvents(): {
      id: number;
      registration_number: string;
      eventType: string;
      date: string;
      remainingDays: number;
      tax_due_date: string | null;
      tax_status: string;
    }[] {
      const events: {
        id: number;
        registration_number: string;
        eventType: string;
        date: string;
        remainingDays: number;
        tax_due_date: string | null;
        tax_status: string;
      }[] = [];

      const today = new Date();

      // Collect MOT expiry events
      this.vehicles.forEach((vehicle) => {
        if (vehicle.mot_expiry_date && vehicle.tax_due_date) {
          const expiryDate = new Date(vehicle.mot_expiry_date);
          const diffTime = expiryDate.getTime() - today.getTime();
          const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
          events.push({
            id: vehicle.id,
            registration_number: vehicle.registration_number,
            eventType: "MOT Expiry",
            date: vehicle.mot_expiry_date,
            remainingDays: diffDays,
            tax_due_date: vehicle.tax_due_date,
            tax_status: vehicle.tax_status,
          });
        }
      });

      // Collect Tax due events
      this.vehicles.forEach((vehicle) => {
        if (vehicle.tax_due_date) {
          const dueDate = new Date(vehicle.tax_due_date);
          const diffTime = dueDate.getTime() - today.getTime();
          const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
          events.push({
            id: vehicle.id,
            registration_number: vehicle.registration_number,
            eventType: "Tax Due",
            date: vehicle.tax_due_date,
            remainingDays: diffDays,
            tax_due_date: vehicle.tax_due_date,
            tax_status: vehicle.tax_status,
          });
        }
      });

      // Sort events by remaining days (from soonest to latest)
      events.sort((a, b) => a.remainingDays - b.remainingDays);

      return events;
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
  },
});
</script>

<style scoped>
.event-list {
  font-family: "Roboto", sans-serif;
}

.event-item {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.event-details {
  display: flex;
  flex-wrap: wrap;
  font-size: x-large;
  text-align: center;
}

.event-info {
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
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-logs {
  background-color: #060606;
  color: white;
  border: none;
  padding: 5px 10px;
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
  padding: 20px;
  font-weight: bold;
  text-align: center;
}

.expired {
  color: #c60000;
}

.valid {
  color: #008a15;
}
</style>
