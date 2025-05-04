import { createApp } from 'vue';
import App from './App.vue';

// Viox
import router from './router'
import store from './store'
import axios from 'axios'


const token = localStorage.getItem('token')
if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    store.dispatch('auth/fetchCurrentUser')
}

const app = createApp(App);
app.use(store)
app.use(router);
app.mount('#app');
