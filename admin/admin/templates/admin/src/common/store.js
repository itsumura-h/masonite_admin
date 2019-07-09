import { connect, createStore } from 'undux'
import Const from '../common/const';

export const store = createStore({
  drawerOpen: true,
  drawerWidth: Const.drawerWidth,
  info: {},
  modelStr: {},
  targetId: 0,
  rowsPerPage: 10,
});

export const withStore = connect(store);
