import { createRouter, createWebHistory } from 'vue-router'

// Components und Views
import testlabView from '../views/Testlab.vue'
import Register from '../components/Register.vue'
import bookAppointment from '../components/bookAppointment.vue'
import UserList from '../components/UserList.vue'
import Coverpage from '../views/Coverpage.vue'
import AppointmentCalender from '../views/AppointmentCalender.vue'
import AuthModal from '@/components/AuthModal.vue'

const routes = [
  { path: '/', component: Coverpage },
  { path: '/testlab', name: 'testlab', component: testlabView },
  { path: '/register', component: Register },
  { path: '/book', component: bookAppointment },
  { path: '/users', component: UserList },
  { path: '/appointment-calender', component: AppointmentCalender },
  { path: '/authmodal', component: AuthModal, props: true }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
