<script setup>
import AlertTableComp from '../components/AlertTableComponent.vue'

</script>

<template>
  <div>
    <h1>Enter Your Email to see the alerts associated with it:</h1>
    <form @submit.prevent="submitForm">
      <label for="email">Email:</label>
      <input type="email" v-model="email" id="email" name="email">
      <button type="submit">Submit</button>
    </form>
    <div id="TextArea">
      <h2>{{ alertMessage }}</h2>
    </div>
    <div>
      <AlertTableComp :alertArr="alertArr" @removeAlert="removeAlert"/>
    </div>
  </div>
</template>

<script>
// AlertTableComp.doSearch(0, 20, "id", "asc");
export default {
  data() {
    return {
      email: '',
      alertMessage: '',
      alertArr: []
    };
  },
  methods: {
    async getAlerts(email) {
      try {
        const targetUrl = `http://localhost:3000/api/getalerts/${email}`;
        const response = await fetch(targetUrl);

        if (!response.ok) {
          throw new Error('Failed to fetch');
        }
        this.alertArr = await response.json();
        if (this.alertArr.length === 0) {
          this.alertMessage = "No alerts found for this email.";
        } else {
          this.alertMessage = ""; // Clear the message if there are alerts
        }
      } catch (error) {
        console.log("Failed to fetch alerts:", error);
        this.alertMessage = "An error occurred while fetching alerts.";
      }
    },
    async removeAlert(alert) {
      try{
        console.log(alert);
        let response = await fetch('http://localhost:3000/remove-alert', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(alert)
        })
        let data = await response.json();
        console.log(data);
        this.getAlerts(this.email);
        // .then(response => response.json())
        // .then(data => console.log(data))
        // .then(this.getAlerts())
        // .catch(error => console.error('Error:', error));
      }
      catch (error){
        console.error("Error:", error);
      }
    },
    submitForm() {
      if (this.email) {
        this.getAlerts(this.email);
      } else {
        console.log('Email is required');
      }
    }
  }
}
</script>

<style scoped>

</style>