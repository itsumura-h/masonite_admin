import Vue from 'vue'
import Vuex from 'vuex'
import CONST from './common/const'
import Util from './common/util'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    drawerOpen: true,
    drawerWidth: 0,
    info: {}
  },
  mutations: {
    // 同期処理
    drawerOpen (state) {
      state.drawerOpen = !state.drawerOpen
      state.drawerWidth = state.drawerOpen ? 0 : CONST.drawerWidth
    },
    getInfo (state) {
      Util.getAPI('/admin/api/info')
        .then(response => {
          state.info = response.data
        })
    }
  },
  actions: {
    // 非同期処理
  }
})
