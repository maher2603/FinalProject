<template>
  <div class="vehicle-list">
    <div v-if="-1 > 0"></div>
    <div v-else>
      <p class="start-text">Add a log to get started</p>
    </div>
  </div>
</template>

<script lang="ts"></script>

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
  padding: 20px;
  font-weight: bold;
  text-align: center;
}
</style>
