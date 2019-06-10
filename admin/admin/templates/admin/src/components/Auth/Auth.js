import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import {withStore} from '../../common/store';

class Auth extends React.Component {

  render() {
    if(!window.localStorage.getItem('login_id') || !window.localStorage.getItem('login_token')){
      return <Redirect to={'/admin/login'} />
    }else{
      return <Route children={this.props.children} />
    }
  }
}

export default withStore(Auth);