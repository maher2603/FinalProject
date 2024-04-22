<template>
  <div class="event-list">
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

          if (diffDays === 30) {
            this.sendEmailReminder(
              vehicle.registration_number,
              "MOT expires",
              diffDays
            );
          }
        }
      });

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

          if (diffDays === 30) {
            this.sendEmailReminder(
              vehicle.registration_number,
              "Tax is due",
              diffDays
            );
          }
        }
      });

      events.sort((a, b) => a.remainingDays - b.remainingDays);

      return events;
    },
  },
  mounted() {
    // Call getVehicles method when the component is mounted
    this.getVehicles();
    // this.vehicles.forEach((vehicle) => {
    //   if (vehicle.mot_expiry_date && vehicle.tax_due_date) {
    //     const today = new Date();
    //     const reminderDays = 30;
    //     const expiryDate = new Date(vehicle.mot_expiry_date);
    //     const taxDueDate = new Date(vehicle.tax_due_date);
    //     const diffTimeMot = expiryDate.getTime() - today.getTime();
    //     const diffTimeTax = taxDueDate.getTime() - today.getTime();
    //     const diffDaysMot = Math.ceil(diffTimeMot / (1000 * 60 * 60 * 24));
    //     const diffDaysTax = Math.ceil(diffTimeTax / (1000 * 60 * 60 * 24));
    //     const scheduleMot = diffDaysMot - reminderDays;
    //     const scheduleTax = diffDaysTax - reminderDays;

    //     if (diffDaysMot >= 30) {
    //       this.scheduleEmailReminder(
    //         vehicle.registration_number,
    //         "MOT expires",
    //         scheduleMot
    //       );
    //     }

    //     if (diffDaysTax >= 30) {
    //       this.scheduleEmailReminder(
    //         vehicle.registration_number,
    //         "Tax is due",
    //         scheduleTax
    //       );
    //     }
    //   }
    // });
    // console.log("Component mounted");
  },
  methods: {
    async getVehicles() {
      try {
        const response = await fetch("http://localhost:8000/get-vehicles/", {
          method: "GET",
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
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
    // async scheduleEmailReminder(
    //   registrationNumber: string,
    //   eventType: string,
    //   scheduledDays: number
    // ) {
    //   try {
    //     const today = new Date();
    //     const sendDate = new Date(
    //       today.getTime() + scheduledDays * 24 * 60 * 60 * 1000
    //     );

    //     const requestBody = {
    //       message: `Your vehicle ${registrationNumber}'s ${eventType} in 30 days.`,
    //       sendDate: sendDate.toISOString(),
    //     };

    //     console.log("Request Body:", requestBody); // Log request body for debugging

    //     const response = await fetch("http://localhost:8000/send-email/", {
    //       method: "POST",
    //       credentials: "include",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify(requestBody),
    //     });

    //     if (response.ok) {
    //       console.log("Email reminder scheduled successfully.");
    //     } else {
    //       const errorResponse = await response.json(); // Parse error response if available
    //       console.error(
    //         "Failed to schedule email reminder:",
    //         response.status,
    //         errorResponse
    //       );
    //     }
    //   } catch (error) {
    //     console.error("Error scheduling email reminder:", error);
    //   }
    // },
    async sendEmailReminder(
      registrationNumber: string,
      eventType: string,
      remainingDays: number
    ) {
      try {
        const response = await fetch("http://localhost:8000/send-email/", {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: `Your vehicle ${registrationNumber}'s ${eventType} in ${remainingDays} days.`,
          }),
        });
        if (response.ok) {
          console.log("Email sent successfully.");
        } else {
          console.error(
            "Failed to send email:",
            response.status,
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error sending email:", error);
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
</style>
