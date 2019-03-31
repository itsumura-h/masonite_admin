import { connect, createStore } from 'undux'
import Const from '../common/const';

const store = createStore({
})

export const withStore = connect(store)
