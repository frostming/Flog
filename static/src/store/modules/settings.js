import defaultSettings from '@/settings'
import { changeTheme, getTheme } from '@/api/user'
const { showSettings, tagsView, fixedHeader, sidebarLogo, theme } = defaultSettings

const state = {
  theme: theme,
  showSettings: showSettings,
  tagsView: tagsView,
  fixedHeader: fixedHeader,
  sidebarLogo: sidebarLogo
}

const mutations = {
  CHANGE_SETTING: (state, { key, value }) => {
    if (state.hasOwnProperty(key)) {
      state[key] = value
    }
  }
}

const actions = {
  changeSetting({ commit }, data) {
    const { key, value } = data
    if (key === 'theme') {
      changeTheme(value)
    }
    commit('CHANGE_SETTING', data)
  },
  getTheme({ commit }) {
    getTheme().then(value => {
      commit('CHANGE_SETTING', { key: 'theme', value })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
