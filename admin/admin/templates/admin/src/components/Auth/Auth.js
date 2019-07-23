import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import {withStore} from '../../common/store';

const Auth=(props)=>{
  if(!window.localStorage.getItem('login_id') ||
      !window.localStorage.getItem('login_token') ||
      !window.localStorage.getItem('login_permission')
  ){
    return <Redirect to={'/admin/login'} />
  }else{
    return <Route children={props.children} />
  }
}

export default withStore(Auth);