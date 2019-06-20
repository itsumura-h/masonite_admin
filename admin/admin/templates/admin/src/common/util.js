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

    const newParams = new FormData();
    Object.keys(params).forEach((key)=>{
      newParams.append(key, params[key]);
    });

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

    const newParams = new FormData();
    Object.keys(params).forEach((key)=>{
      newParams.append(key, params[key]);
    });

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

    const newParams = new FormData();
    Object.keys(params).forEach((key)=>{
      newParams.append(key, params[key]);
    });

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

    const params = new FormData();
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
    if(error.response && error.response.status === 403){
      window.localStorage.removeItem('login_id');
      window.localStorage.removeItem('login_token');
      window.localStorage.removeItem('login_name');
      window.location.href = '/admin/login';
    }
  }

  static dateToString=(date, format)=>{
    format = format.replace(/YYYY/, date.getFullYear());
    format = format.replace(/MM/, date.getMonth() + 1);
    format = format.replace(/DD/, date.getDate());
    return format;
  }
}