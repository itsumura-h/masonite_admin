import { connect, createStore } from 'undux'
import Const from '../common/const';

const store = createStore({
  drawerOpen: true,
  drawerWidth: Const.drawerWidth,
  models: [],
  topppageData: {},
})

export const withStore = connect(store)
