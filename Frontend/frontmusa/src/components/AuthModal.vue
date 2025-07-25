<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal">
      <div class="modal-header">
        <h2 v-if="activeTab === 'login'">Login</h2>
        <h2 v-else>Registrierung</h2>
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
        <div>      
          <GoogleSignIn @signed-in="handleSignIn" @signed-out="handleGoogleSignOut" />
        </div>
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
  
<script>
import axios from "axios";
import { setToken } from "../auth";
import { API_ENDPOINTS } from "../config";
import GoogleSignIn from '@/components/GoogleSignIn.vue';
import { signOutGoogle } from '@/plugins/googleAuth';

export default {
  name: "AuthModal",
  components: {
    GoogleSignIn,
  },
  data() {
    return {
      activeTab: "login",
      loginData: {
        email: "",
        password: "",
      },
      registerData: {
        name: "",
        email: "",
        phonenumber: "",
        password: "",
      },
    };
  },
  methods: {
    handleSignIn(payload) {
      console.log('Nutzer angemeldet:', payload);
      // Hier kannst du z. B. das Token im Vuex-Store speichern oder direkt ans Backend schicken.
    },
    closeModal() {
      this.$emit("close");
    },
    created() {
      this.tryAutoLogin();
    },
    async tryAutoLogin() {
      const token = localStorage.getItem("access_token");
      if (!token) return;
      try {
        const meRes = await axios.get(API_ENDPOINTS.ME, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const currentUser = meRes.data;
        this.$emit("user-logged-in", currentUser);
        this.closeModal();
      } catch (err) {
        console.error("Auto-Login fehlgeschlagen", err);
        localStorage.removeItem("access_token");
      }
    },

    async handleLogin() {
      try {
        const loginRes = await axios.post(API_ENDPOINTS.LOGIN, this.loginData, {
          headers: { "Content-Type": "application/json" },
          withCredentials: true,
        });
        setToken(loginRes.data.access_token);
        localStorage.setItem("access_token", loginRes.data.access_token);

        const usersRes = await axios.get(API_ENDPOINTS.USERS, {
          headers: {
            Authorization: `Bearer ${loginRes.data.access_token}`,
          },
        });
        const allUsers = usersRes.data;

        const currentUser = allUsers.find(
          (u) => u.email.toLowerCase() === this.loginData.email.toLowerCase()
        );
        if (!currentUser) {
          throw new Error("User nicht gefunden!");
        }

        console.log(
          "Eingeloggt als:",
          currentUser.name,
          "(ID:",
          currentUser.id,
          ")"
        );
        this.$emit("user-logged-in", currentUser);

        alert("Login erfolgreich!");
        this.closeModal();
      } catch (error) {
        console.error("Login/Register error:", error);
        alert("Login fehlgeschlagen!");
      }
    },

    async handleRegister() {
      try {
        const response = await axios.post(
          API_ENDPOINTS.REGISTER,
          this.registerData,
          {
            headers: { "Content-Type": "application/json" },
            withCredentials: true,
          }
        );
        alert("Registrierung erfolgreich! Bitte melde dich an.");
        this.activeTab = "login";
      } catch (error) {
        console.error("Registrierung error:", error);
        alert("Registrierung fehlgeschlagen!");
      }
    },
    async handleGoogleSignOut() {
      try {
        await signOutGoogle();
        this.closeModal();
      } catch (error) {
        console.error('Logout fehlgeschlagen:', error);
        alert('Logout fehlgeschlagen!');
      }
    },
  },
};
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
</style>