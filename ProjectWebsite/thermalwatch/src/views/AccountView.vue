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
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      alertMessage: ''
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

        let alertArray = await response.text();
        if (alertArray.length === 0) {
          this.alertMessage = "No alerts found for this email.";
        } else {
          this.alertMessage = ""; // Clear the message if there are alerts
        }
        console.log(alertArray);
      } catch (error) {
        console.log("Failed to fetch alerts:", error);
        this.alertMessage = "An error occurred while fetching alerts.";
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

