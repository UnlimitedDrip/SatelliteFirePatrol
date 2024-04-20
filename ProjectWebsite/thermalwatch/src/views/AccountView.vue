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
