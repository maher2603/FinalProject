<template>
  <div class="container-fluid p-0">
    <!-- Animated background -->
    <div class="animated-background">
      <div class="container">
        <div class="row justify-content-center main-content">
          <div class="col-md-8">
            <h1>Welcome to Whips&Gigs</h1>
            <p>Your destination for all things vehicles!</p>
          </div>
        </div>
      </div>
    </div>
    <!-- Description section -->
    <div class="description-section">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <h2>What We Offer</h2>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
              tincidunt sit amet odio vitae bibendum. Duis dignissim lacus eget
              dolor dictum, et malesuada felis condimentum.
            </p>
            <p>
              Nullam id quam ac quam aliquet auctor. Proin eget risus vitae urna
              laoreet mattis in at velit. Phasellus porttitor gravida libero,
              non scelerisque sapien porttitor at.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<style>
/* Additional CSS styles */
.bg-theme {
  background-color: #141414;
}
/* Animated background */
.animated-background {
  overflow: hidden;
  position: relative;
  background-color: #141414;
  animation: changeColor 10s infinite alternate;
}
@keyframes changeColor {
  0% {
    background-color: #141414;
  }
  50% {
    background-color: #333;
  }
  100% {
    background-color: #141414;
  }
}
/* Modern styling for the main content */
.main-content {
  padding: 100px 0;
  text-align: center;
  color: #fff;
}
.main-content h1 {
  font-size: 3rem;
  margin-bottom: 20px;
}
.main-content p {
  font-size: 1.5rem;
  margin-bottom: 40px;
}
/* Description section */
.description-section {
  background-color: #f8f9fa; /* Light gray background */
  padding: 50px 0;
  text-align: center;
}
</style>
