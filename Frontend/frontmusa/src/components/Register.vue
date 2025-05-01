<template>
  <div class="register-container">
    <div class="register-card">
      <h2>Registrieren</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="name">Name</label>
          <input
            id="name"
            v-model="name"
            placeholder="Ihr vollständiger Name"
            required
          />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            type="email"
            v-model="email"
            placeholder="Ihre Email-Adresse"
            required
          />
        </div>
        <div class="form-group">
          <label for="phonenumber">Telefonnummer</label>
          <input
            id="phonenumber"
            v-model="phonenumber"
            placeholder="Ihre Telefonnummer"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Passwort</label>
          <input
            id="password"
            type="password"
            v-model="password"
            placeholder="Wählen Sie ein sicheres Passwort"
            required
          />
        </div>
        <button type="submit">Registrieren</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return { name: "", email: "", phonenumber: "", password: "" };
  },
  methods: {
    async register() {
      try {
        await axios.post("http://192.168.178.104:5000/register", {
          name: this.name,
          email: this.email,
          phonenumber: this.phonenumber,
          password: this.password,
        });
        alert("Registrierung erfolgreich!");
      } catch (error) {
        console.error("Registration error:", error);
        alert(`Fehler bei der Registrierung: ${error.message}`);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
        }
      }
    },
  },
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background-color: #f5f5f5;
}

.register-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  color: #333;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

form {
  display: flex;
  flex-direction: column;
}

input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus {
  outline: none;
  border-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

button {
  background-color: #4caf50;
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.1s;
  margin-top: 1rem;
}

button:hover {
  background-color: #45a049;
}

button:active {
  transform: scale(0.98);
}

@media (max-width: 480px) {
  .register-card {
    padding: 1.5rem;
  }

  h2 {
    font-size: 1.5rem;
  }

  input {
    padding: 0.7rem;
  }
}
</style>