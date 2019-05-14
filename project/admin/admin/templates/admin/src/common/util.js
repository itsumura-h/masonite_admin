import React from 'react';
import axios from 'axios';
import CONST from './const';
import {Redirect} from 'react-router-dom';

export default class Util extends React.Component{
  static getAPI=(url, params={})=>{
    url = CONST.APIHOST + url;
    params['login_id'] = window.localStorage.getItem('login_id')
    params['login_token'] = window.localStorage.getItem('login_token')

    return axios.get(url, {params: params})
      .then(response=>{
        this.loginFale(response);
        if(response.headers['content-type'] === 'application/json; charset=utf-8'){
          return response;
        }else{
          return [];
        }
      })
      .catch(err=>{
        console.error(err);
        return [];
      })
  }

  static postAPI=(url, params)=>{
    url = CONST.APIHOST + url;

    params['login_id'] = window.localStorage.getItem('login_id')
    params['login_token'] = window.localStorage.getItem('login_token')

    console.log(params);

    const newParams = new URLSearchParams();
    for(let key in params){
      const param = params[key];
      newParams.append(key, param);
    }

    return axios.post(url, newParams)
      .then(response=>{
        this.loginFale(response);
        return response;
      })
      .catch(err=>{
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
        this.loginFale(response);
        return response;
      })
      .catch(err=>{
        console.error(err);
        return [];
      })
  }

  static loginFale=(response)=>{
    if('login' in response.data && response.data.login == false){
      window.location.href = '/admin/login';
    }
  }
}