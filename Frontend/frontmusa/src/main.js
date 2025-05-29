import { createApp } from 'vue';
import App from './App.vue';
import router from './router'
import store from './store'
import axios from 'axios'
import { API_BASE_URL } from './config'
import { loadGoogleAuth } from './plugins/googleAuth'

// Set axios defaults
axios.defaults.baseURL = API_BASE_URL

const token = localStorage.getItem('token')
if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    store.dispatch('auth/fetchCurrentUser')
}

const app = createApp(App);
app.use(store)
app.use(router);

loadGoogleAuth()
  .then(() => {
    app.mount('#app');
  })
  .catch((err) => {
    console.error('Google Auth Initialization failed', err);
    app.mount('#app');
  });
