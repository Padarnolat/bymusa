import axios from 'axios'
import { API_ENDPOINTS } from '../../config'

const state = { user: null }
const mutations = {
    setUser(state, user) { state.user = user }
}
const actions = {
    async login({ commit }, credentials) {
        const { data } = await axios.post(API_ENDPOINTS.LOGIN, credentials)
        localStorage.setItem('token', data.token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${data.token}`
        const { data: user } = await axios.get(API_ENDPOINTS.ME)
        commit('setUser', user)
    },
    async fetchCurrentUser({ commit }) {
        const { data: user } = await axios.get(API_ENDPOINTS.ME)
        commit('setUser', user)
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}