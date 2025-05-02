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
import { setToken } from "../auth"; // Importiere deine Auth-Manager-Funktionen

export default {
  name: "AuthModal",
  props: {
    currentUser: {
      type: Object,
      default: () => null,
    },
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
    closeModal() {
      this.$emit("close");
    },
    async handleLogin() {
      try {
        const loginRes = await axios.post(
          "http://192.168.178.104:5000/login",
          this.loginData,
          {
            headers: { "Content-Type": "application/json" },
            withCredentials: true,
          }
        );
        setToken(loginRes.data.access_token);

        // Jetzt alle User holen
        const usersRes = await axios.get("http://192.168.178.104:5000/users", {
          headers: {
            // falls benötigt:
            Authorization: `Bearer ${loginRes.data.access_token}`,
          },
        });
        const allUsers = usersRes.data;

        // per E-Mail den gerade eingeloggten finden
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
          "http://192.168.178.104:5000/register",
          this.registerData,
          {
            headers: { "Content-Type": "application/json" },
            withCredentials: true,
          }
        );
        alert("Registrierung erfolgreich! Bitte melde dich an.");
        // Nach erfolgreicher Registrierung zum Login-Tab wechseln
        this.activeTab = "login";
      } catch (error) {
        console.error("Registrierung error:", error);
        alert("Registrierung fehlgeschlagen!");
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