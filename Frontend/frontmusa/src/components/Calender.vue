<template>
  <div class="calendar-wrapper">
    <FullCalendar :options="calendarOptions" />
  </div>
</template>

<script>
import axios from "axios";
import FullCalendar from "@fullcalendar/vue3";
import timeGridPlugin from "@fullcalendar/timegrid";
import dayGridPlugin from "@fullcalendar/daygrid";
import deLocale from "@fullcalendar/core/locales/de";
import { API_ENDPOINTS } from "../config";

export default {
  components: {
    FullCalendar,
  },
  data() {
    return {
      calendarOptions: {
        plugins: [timeGridPlugin, dayGridPlugin],
        initialView: "timeGridWeek",
        hiddenDays: [0, 1, 3, 5, 6],
        slotMinTime: "09:00:00",
        slotMaxTime: "19:00:00",
        allDaySlot: false,
        locale: deLocale,
        slotLabelFormat: {
          hour: "2-digit",
          minute: "2-digit",
          omitZeroMinute: false,
          meridiem: false,
        },
        expandRows: true,
        events: [],
        eventContent: (arg) => ({
          html: `
            <div class="custom-event">
              <strong>${arg.event.title}</strong>
              <div>${arg.timeText}</div>
            </div>`,
        }),
      },
      appointments: [],
    };
  },
  methods: {
    async fetchAppointments() {
      try {
        const response = await axios.get(API_ENDPOINTS.APPOINTMENTS);
        this.appointments = response.data;
      } catch (error) {
        console.error("Error fetching appointments:", error);
      }
    },
  },
  mounted() {
    this.fetchAppointments();
  },
};
</script>

<style scoped>
.calendar-wrapper {
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
}

:deep(.fc) {
  font-family: "Inter", sans-serif;
  font-size: 14px;
  background: #fff;
  border-radius: 8px;
}

:deep(.fc-toolbar-title) {
  font-size: 1.25rem;
  font-weight: 600;
  color: #222;
}

:deep(.fc-event) {
  border: none;
  border-radius: 6px;
  background-color: #2e7d32 !important;
  padding: 4px 6px;
  transition: background 0.2s ease;
}

:deep(.fc-event:hover) {
  background-color: #1b5e20 !important;
}

:deep(.custom-event) {
  display: flex;
  flex-direction: column;
  font-size: 13px;
  color: #fff;
  gap: 2px;
}

:deep(.fc-timegrid-slot-label) {
  color: #666;
  font-size: 12px;
}

:deep(.fc-scrollgrid) {
  border: none;
}

:deep(.fc-col-header-cell-cushion) {
  color: #333;
  font-weight: 500;
}

:deep(.fc-timegrid-slot) {
  border-color: #eee;
}
</style>
