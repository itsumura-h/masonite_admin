import axios from 'axios'
import CONST from './const'

export default class Util {
  static getAPI=(url, params = {}) => {
    url = CONST.APIHOST + url
    params['login_id'] = window.localStorage.getItem('login_id')
    params['login_token'] = window.localStorage.getItem('login_token')

    return axios.get(url, { params: params })
      .then(response => {
        return response
      })
      .catch(err => {
        // this.loginFale(err)
        console.error(err)
        return []
      })
  }
}
