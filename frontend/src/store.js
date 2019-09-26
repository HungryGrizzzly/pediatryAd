import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    logged: false
  },
  mutations: {

  },
  actions: {

  },
  getters: {
    LOGGED: state => state.logged
  }
})

export default store