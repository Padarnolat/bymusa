<template>
  <div class="appointment-container">
    <div class="appointment-card">
      <h2>Termin buchen</h2>
      <form @submit.prevent="bookAppointment">
        <div class="form-group">
          <label for="user_id">Benutzer-ID</label>
          <input
            id="user_id"
            v-model="user_id"
            placeholder="Ihre Benutzer-ID"
            required
          />
        </div>
        <div class="form-group">
          <label for="barber_id">Friseur-ID</label>
          <input
            id="barber_id"
            v-model="barber_id"
            placeholder="Wählen Sie einen Friseur"
            required
          />
        </div>
        <div class="form-group">
          <label for="appointment_date">Datum</label>
          <input
            id="appointment_date"
            type="date"
            v-model="appointment_date"
            required
          />
        </div>
        <div class="form-group">
          <label for="appointment_time">Uhrzeit</label>
          <input
            id="appointment_time"
            type="time"
            v-model="appointment_time"
            required
          />
        </div>
        <button type="submit">Termin buchen</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { API_ENDPOINTS } from "../config";

export default {
  data() {
    return {
      user_id: "",
      barber_id: "",
      appointment_date: "",
      appointment_time: "",
    };
  },
  methods: {
    async bookAppointment() {
      try {
        const formattedTime = this.appointment_time + ":00";

        const response = await axios.post(
          API_ENDPOINTS.BOOK_APPOINTMENT,
          {
            user_id: this.user_id,
            barber_id: this.barber_id,
            appointment_date: this.appointment_date,
            appointment_time: formattedTime,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
            withCredentials: true,
          }
        );

        if (response.status === 201) {
          alert("Termin erfolgreich gebucht!");
        }
      } catch (error) {
        console.error("Booking error:", error);
        let errorMessage = "Ein Fehler ist aufgetreten.";

        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
          errorMessage = error.response.data.error || errorMessage;
        }

        alert(`Fehler bei der Buchung: ${errorMessage}`);
      }
    },
  },
};
</script>

<style scoped>
.appointment-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background-color: #f5f5f5;
}

.appointment-card {
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
  .appointment-card {
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