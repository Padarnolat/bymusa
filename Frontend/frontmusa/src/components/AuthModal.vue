<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal">
      <!-- Fehlermeldung und Ladeanzeige -->
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="isLoading" class="loading-spinner">Lade...</div>

      <div class="modal-header">
        <h2>{{ activeTab === "login" ? "Login" : "Registrierung" }}</h2>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>

      <div class="modal-tabs">
        <button
          :class="{ active: activeTab === 'login' }"
          @click="activeTab = 'login'"
        >
          Login
        </button>
        <button
          :class="{ active: activeTab === 'register' }"
          @click="activeTab = 'register'"
        >
          Registrieren
        </button>
      </div>

      <div class="modal-content">
        <!-- Login-Formular -->
        <form v-if="activeTab === 'login'" @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="login-email">Email</label>
            <input
              id="login-email"
              v-model="loginData.email"
              type="email"
              required
            />
          </div>
          <div class="form-group">
            <label for="login-password">Passwort</label>
            <input
              id="login-password"
              v-model="loginData.password"
              type="password"
              required
            />
          </div>
          <button type="submit">Login</button>
        </form>

        <!-- Registrierungs-Formular -->
        <form v-else @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="register-name">Name</label>
            <input
              id="register-name"
              v-model="registerData.name"
              type="text"
              required
            />
          </div>
          <div class="form-group">
            <label for="register-email">Email</label>
            <input
              id="register-email"
              v-model="registerData.email"
              type="email"
              required
            />
          </div>
          <div class="form-group">
            <label for="register-phonenumber">Telefonnummer</label>
            <input
              id="register-phonenumber"
              v-model="registerData.phonenumber"
              type="text"
              required
            />
          </div>
          <div class="form-group">
            <label for="register-password">Passwort</label>
            <input
              id="register-password"
              v-model="registerData.password"
              type="password"
              required
            />
          </div>
          <button type="submit">Registrieren</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import axios from "axios";
import { auth, setToken } from "../auth.js";

// Reactive State
const activeTab = ref("login");
const loginData = ref({ email: "", password: "" });
const registerData = ref({
  name: "",
  email: "",
  phonenumber: "",
  password: "",
});
const isLoading = ref(false);
const errorMessage = ref("");

// Computed für Auth
const user = computed(() => auth.user || {});

// Methods
async function handleLogin() {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    const resp = await axios.post(
      "http://192.168.178.104:5000/login",
      loginData.value
    );
    const token = resp.data.access_token;

    // Nutzer-Daten abrufen
    const meResp = await axios.get("http://192.168.178.104:5000/me", {
      headers: { Authorization: "Bearer " + token },
    });

    setToken(token, meResp.data);
    alert("Login erfolgreich!");
    closeModal();
  } catch (err) {
    console.error("Login-Error:", err);
    errorMessage.value = err.response?.data?.error || "Login fehlgeschlagen!";
  } finally {
    isLoading.value = false;
  }
}

async function handleRegister() {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    const resp = await axios.post(
      "http://192.168.178.104:5000/register",
      registerData.value,
      { withCredentials: true }
    );
    const token = resp.data.access_token;

    // Nutzer-Daten abrufen
    const meResp = await axios.get("http://192.168.178.104:5000/me", {
      headers: { Authorization: "Bearer " + token },
    });

    setToken(token, meResp.data);
    alert("Registrierung erfolgreich!");
    closeModal();
  } catch (err) {
    console.error("Register-Error:", err);
    errorMessage.value =
      err.response?.data?.error || "Registrierung fehlgeschlagen!";
  } finally {
    isLoading.value = false;
  }
}

function closeModal() {
  // Emit schließt das Modal in der Elternkomponente
  emit("close");
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal {
  background: #fff;
  border-radius: 8px;
  padding: 1rem;
  width: 400px;
  max-width: 90%;
  position: relative;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.close-btn {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}
.modal-tabs {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}
.modal-tabs button {
  flex: 1;
  padding: 0.5rem;
  cursor: pointer;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
}
.modal-tabs button.active {
  border-bottom: 2px solid #4caf50;
  font-weight: bold;
}
.modal-content {
  margin-top: 1rem;
}
.form-group {
  margin-bottom: 1rem;
}
input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}
.error-message {
  color: red;
  margin-bottom: 0.5rem;
}
.loading-spinner {
  margin-bottom: 0.5rem;
}
</style>
