import React from 'react';
import axios from 'axios';
import CONST from './const';

export default class Util extends React.Component{
  static getAPI=(url, params={})=>{
    url = CONST.APIHOST + url;
    params['login_id'] = window.localStorage.getItem('login_id')
    params['login_token'] = window.localStorage.getItem('login_token')

    return axios.get(url, {params: params})
      .then(response=>{
        if(response.headers['content-type'] === 'application/json; charset=utf-8'){
          return response;
        }else{
          return [];
        }
      })
      .catch(err=>{
        this.loginFale(err);
        console.error(err);
        return [];
      })
  }

  static postAPI=(url, params)=>{
    url = CONST.APIHOST + url;

    params['login_id'] = window.localStorage.getItem('login_id')
    params['login_token'] = window.localStorage.getItem('login_token')

    const newParams = new URLSearchParams();
    for(let key in params){
      const param = params[key];
      newParams.append(key, param);
    }

    return axios.post(url, newParams)
      .then(response=>{
        return response;
      })
      .catch(err=>{
        this.loginFale(err);
        console.error(err);
        return [];
      })
  }

  static deleteAPI=(url)=>{
    url = CONST.APIHOST + url;
    let params = {}
    params['login_id'] = window.localStorage.getItem('login_id')
    params['login_token'] = window.localStorage.getItem('login_token')

    const newParams = new URLSearchParams();
    for(let key in params){
      const param = params[key];
      newParams.append(key, param);
    }

    return axios.post(url, newParams)
      .then(response=>{
        return response;
      })
      .catch(err=>{
        this.loginFale(err);
        console.error(err);
        return [];
      })
  }

  static loginApi=(url, params)=>{
    url = CONST.APIHOST + url;

    const newParams = new URLSearchParams();
    for(let key in params){
      const param = params[key];
      newParams.append(key, param);
    }

    return axios.post(url, newParams)
      .then(response=>{
        return response;
      })
      .catch(err=>{
        console.error(err);
        return [];
      })
  }

  static logoutApi=()=>{
    const url = CONST.APIHOST + '/admin/api/logout';

    const params = new URLSearchParams();
    params.append('login_id', window.localStorage.getItem('login_id'));

    return axios.post(url, params)
      .then(response=>{
        return response;
      })
      .catch(err=>{
        console.error(err);
        return [];
      })
  }

  static loginFale=(error)=>{
    if(error.response.status === 403){
      window.location.href = '/admin/login';
    }
  }
}