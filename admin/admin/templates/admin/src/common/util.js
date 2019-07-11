import React from 'react';
import axios from 'axios';
import CONST from './const';
import {store} from './store';

export default class Util extends React.Component{

  static contentType=()=>{
    return new FormData();
    // return new URLSearchParams();
  }

  static getAPI=(url, params={})=>{
    url = CONST.APIHOST + url;
    params = this.setLoginParamas(params);

    return axios.get(url, {params: params})
      .then(response=>{
        return response;
      })
      .catch(err=>{
        this.loginFale(err);
        console.error(err);
        return [];
      })
  }

  static postAPI=(url, params)=>{
    url = CONST.APIHOST + url;
    params = this.setLoginParamas(params);

    const newParams = this.contentType();
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

  static putAPI=(url, params)=>{
    url = CONST.APIHOST + url;
    params = this.setLoginParamas(params);

    const newParams = this.contentType();
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

  static deleteAPI=(url, params={})=>{
    url = CONST.APIHOST + url;
    params = this.setLoginParamas(params);

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
    params.append('login_token', window.localStorage.getItem('login_token'));

    return axios.post(url, params)
      .then(response=>{
        return response;
      })
      .catch(err=>{
        console.error(err);
        return [];
      })
  }

  static setLoginParamas=(params)=>{
    params['login_id'] = window.localStorage.getItem('login_id');
    params['login_token'] = window.localStorage.getItem('login_token');
    params['permission'] = window.localStorage.getItem('permission');

    return params;
  }

  static loginFale=(error)=>{
    if(error.response && error.response.status === 403){
      window.localStorage.removeItem('login_id');
      window.localStorage.removeItem('login_token');
      window.localStorage.removeItem('login_name');
      window.localStorage.removeItem('permission');
      window.location.href = '/admin/login';
    }
  }

  static dateToString=(date, format)=>{
    format = format.replace(/YYYY/, date.getFullYear());
    format = format.replace(/MM/, date.getMonth() + 1);
    format = format.replace(/DD/, date.getDate());
    return format;
  }

  static setModelTitle=()=>{
    const model_en_url = window.location.pathname.split('/')[2];
    const model_en_store = store.get('modelStr')['en'];

    model_en_url !== model_en_store &&
    Object.keys(store.get('info')).length > 0 &&
      store.get('info').models.some(model=>{
        if(window.location.pathname.split('/')[2] === model['en']){
          store.set('modelStr')(model);
          return true;
        }
        return false;
      });
  }
}
