import { createApp } from 'vue';
import App from './App.vue';
import router from './router/router.js';
import vue3GoogleLogin from 'vue3-google-login'

import './assets/main.css';
//will need to change client ID settings to work on thermalwatch.org
const CLIENT_ID = '59031367616-kd650umcl23m9rvv9gk7onunk80c1u94.apps.googleusercontent.com';
const app = createApp(App);

app.use(router);
app.use(vue3GoogleLogin, {
    clientId: CLIENT_ID,
})


app.mount('#app');
