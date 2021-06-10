import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: null,
    secretKey: null
  },
  mutations: {
    save: function (state, { username, secretKey }) {
      state.username = username
      state.secretKey = secretKey
      localStorage.setItem('username', state.username)
      localStorage.setItem('secretKey', state.secretKey)
    },
    delete: function (state) {
      state.username = null
      state.secretKey = null
      localStorage.removeItem('username')
      localStorage.removeItem('secretKey')
    }
  },
  actions: {
    load: function ({ commit }) {
      const username = localStorage.getItem('username')
      const secretKey = localStorage.getItem('secretKey')
      if (username && secretKey) {
        commit(
          'save',
          {
            username,
            secretKey: Uint8Array.from(secretKey.split(','))
          }
        )
      }
    },
    login: function ({ commit }, { username, secretKey }) {
      commit('save', { username, secretKey })
    },
    logout: function ({ commit }) {
      commit('delete')
    }
  }
})
