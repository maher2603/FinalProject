<template>
  <div class="container-fluid p-0">
    <!-- Welcome section -->
    <div class="welcome-section">
      <div class="container">
        <div class="video-wrapper">
          <video class="video" autoplay loop muted>
            <source src="../background1.mp4" type="video/webm" />
            <source src="../background1.mp4" type="video/mp4" />
          </video>
          <div class="video-overlay"></div>
        </div>
        <div class="row justify-content-center main-content">
          <div class="col-md-8 text-center">
            <h1 class="welcome-text">Welcome to Whips & Gigs</h1>
            <p class="sub-text">Manage your cars and have a laugh!</p>
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
            <p>An easy and convenient way to manage your vehicle information</p>
            <p>
              Support for multiple vehicles all of varieties so you can manage
              an entire fleet
            </p>
            <p>
              Up to date and accurate vehicle information sourced directly from
              the Driver and Vehicle Licensing Agency
            </p>
            <p>
              A platform to meet and engage with other members of our community
            </p>
            <br />
            <h2>How to get started</h2>
            <p>If you're yet to make an account, what are you waiting for?</p>
            <p>
              Sign up or Log in using the buttons on the navigation bar to gain
              full access
            </p>
            <p>
              Once you're logged in, head over to Garage to start adding your
              vehicles using our easy search tool
            </p>
            <p>
              Check out the forum to see what other members of the community and
              getting up to.
            </p>
            <p>
              Keep your details updated over at your profile page so you never
              miss a reminder
            </p>
            <p></p>
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
.bg-theme {
  background-color: #141414;
}
.welcome-section {
  position: relative;
  background-color: #141414;
  animation: changeColor 10s infinite alternate;
}

.main-content {
  position: relative;
  z-index: 1;
  padding: 100px 0;
  text-align: center;
  color: #fff;
}
.main-content .welcome-text {
  font-size: 3rem;
  margin-bottom: 20px;
}
.main-content .sub-text {
  font-size: 1.5rem;
  margin-bottom: 40px;
}
/* Description section */
.description-section {
  background-color: #f8f9fa;
  padding: 50px 0;
  text-align: center;
}

.video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  filter: brightness(60%);
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, hsl(0, 0%, 8%), rgba(0, 0, 0, 0) 100%);
}
</style>
