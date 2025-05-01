<template>
  <div class="appointment-calender-view">
    <h1>Friseur-Terminplan</h1>
    <div class="calendar-wrapper">
      <Calendar />
    </div>
  </div>
</template>
  
<script>
import Calendar from "../components/Calender.vue";

export default {
  components: {
    Calendar,
  },
};
</script>

<style scoped>
.appointment-calender-view {
  padding: 2rem;
  background-color: #f5f5f5;
  min-height: 100vh;
}

h1 {
  color: #333;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.calendar-wrapper {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .appointment-calender-view {
    padding: 1rem;
  }

  .calendar-wrapper {
    padding: 1rem;
  }

  h1 {
    font-size: 1.5rem;
  }
}
</style>
  