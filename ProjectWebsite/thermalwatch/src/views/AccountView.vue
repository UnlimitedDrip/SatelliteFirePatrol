<<<<<<< HEAD

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
  
=======
<template>
  <div>
    <div v-if="loggedIn">
      
      <button @click='logOut'>Logout</button>
      <h2>Name: {{ user.name }}</h2>
      <h2>Email: {{ user.email }}</h2>
    </div>
    
    <GoogleLogin :callback="callback" prompt auto-login/>

  </div>
</template>

<script>
// I used this tutorial for this implementation: https://youtu.be/hQ5aqvTEqxU?si=PtJwUNVTLvjB-ipB
import { decodeCredential , googleLogout} from 'vue3-google-login'
export default{
  data(){
    return{
      loggedIn:false,
      user:null,

      callback: (response) => {
        console.log("Logged In");
        this.loggedIn = true;
        console.log(response);
        this.user = decodeCredential(response.credential);
      }
    }
  },
  methods:{
    logOut() {
      googleLogout(),
      this.loggedIn = false
    }
  }
}

</script>
<style scoped>
a {
  color: black;
}
button {
  color: black;
}

</style>
>>>>>>> 5c03f95342935c3b3cf36cef3e924cad90b8afcd
