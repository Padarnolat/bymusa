import { createRouter, createWebHistory } from 'vue-router'
import testlabView from '../views/Testlab.vue'
import Register from '../components/Register.vue'
import bookAppointment from '../components/bookAppointment.vue'
import UserList from '../components/UserList.vue'
import Coverpage from '../views/Coverpage.vue'
import AppointmentCalender from '../views/AppointmentCalender.vue'

const routes = [
  { path: '/', component: Coverpage },
  {
    path: '/testlab',
    name: 'testlab',
    component: testlabView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  { path: '/register', component: Register },
  { path: '/book', component: bookAppointment },
  { path: '/users', component: UserList },
  { path: '/appointment-calender', component: AppointmentCalender },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
