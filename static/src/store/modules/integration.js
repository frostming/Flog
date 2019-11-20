import { fetchIntegration, updateIntegration } from '@/api/user'

const state = {
  comment: {
    enabled: false
  },
  disqus: {
    enabled: false,
    shortname: ''
  },
  google_analytics: {
    enabled: false,
    id: ''
  },
  cos: {
    enabled: false,
    secret_id: '',
    secret_key: '',
    bucket: '',
    region: ''
  }
}

const mutations = {
  'SET_INTEGRATION': (state, { name, ...data }) => {
    state[name] = data
  }
}

const actions = {
  fetchData({ commit }) {
    fetchIntegration().then(resp => {
      Object.entries(resp.data).forEach(item => {
        commit('SET_INTEGRATION', { name: item[0], ...item[1] })
      })
    })
  },
  updateData({ commit }, data) {
    commit('SET_INTEGRATION', data)
    return updateIntegration(data)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
