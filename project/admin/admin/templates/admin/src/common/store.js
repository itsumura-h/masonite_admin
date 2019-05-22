import { connect, createStore } from 'undux'
import Const from '../common/const';

const store = createStore({
  drawerOpen: true,
  drawerWidth: Const.drawerWidth,
  info: {},
  targetId: 0,
  rowsPerPage: 10,
})

export const withStore = connect(store)