// Chatgpt code

import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import Register from './components/Register.vue';
import bookAppointment from './components/bookAppointment.vue';
import router from './router';
import AppointmentCalender from './views/AppointmentCalender.vue';
const routes = [
    { path: '/register', component: Register },
    { path: '/book', component: bookAppointment },
    { path: '/appointment-calender', component: AppointmentCalender }
];

// const router = createRouter({
//     history: createWebHistory(),
//     routes
// });

const app = createApp(App);
app.use(router);
app.mount('#app');

//  ISt bevor chatgpt

// import { createApp } from 'vue'
// import App from './App.vue'
// import router from './router'

// createApp(App).use(router).mount('#app')
