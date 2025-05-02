<template>
  <div id="app">
    <nav class="navbar">
      <router-link to="/">Home</router-link> |
      <router-link to="/testlab">Testlab</router-link> |
      <router-link to="/users">Users</router-link> |
      <router-link to="/appointment-calendar">Terminkalender</router-link>

      <div class="auth-status">
        <template v-if="isAuthenticated">
          <span>Hallo, {{ auth.user.name || "User" }}</span>
          <button @click="logout">Logout</button>
        </template>
        <template v-else>
          <button @click="openAuthModal">Login</button>
        </template>
      </div>
    </nav>

    <!-- Auth-Modal -->
    <AuthModal v-if="showAuthModal" @close="closeAuthModal" />

    <router-view />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import AuthModal from "./components/AuthModal.vue";
import { auth, clearToken } from "./auth.js";

// Steuerung des Auth-Modals
const showAuthModal = ref(false);
function openAuthModal() {
  showAuthModal.value = true;
}
function closeAuthModal() {
  showAuthModal.value = false;
}

// Reactive Auth-Status
const isAuthenticated = computed(() => !!auth.token);

// Logout-Funktion
function logout() {
  clearToken();
}
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f5f5f5;
}
.navbar a {
  font-weight: bold;
  color: #2c3e50;
  margin-right: 8px;
}
.navbar a.router-link-exact-active {
  color: #42b983;
}
.auth-status {
  display: flex;
  align-items: center;
  gap: 10px;
}
button {
  cursor: pointer;
}
</style>
