
<template>
    <div>
      <meta name="google-signin-client_id" content="59031367616-kd650umcl23m9rvv9gk7onunk80c1u94.apps.googleusercontent.com">
      <h1>Account</h1>
      <div class="g-signin2" data-onsuccess="onSignIn"></div>
      <a href="#" click="signOut();">Sign out</a>

    </div>
  </template>
  
  <script>
  /* eslint-disable */
  export default {
    mounted() {
      // Load the Google Platform Library
      const script = document.createElement("script");
      script.src = "https://apis.google.com/js/platform.js";
      script.async = true;
      script.async = true;
      script.onload = this.initGoogleAuth(); // Call initGoogleAuth when script is loaded
      document.body.appendChild(script);
    },
    methods: {
      initGoogleAuth() {
        gapi.load('auth2', function(){
          gapi.auth2.init();
        });
      }
    
  }
  
}
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
  }


/* eslint-enable */
</script>

  
<style scoped>
.signin {
  color: red;
}
</style>
  