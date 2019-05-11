import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import {withStore} from './common/store';

import Login from './components/Auth/Login';
import Admin from './components/Admin';

class App extends React.Component {

  render(){
    return(
      <BrowserRouter>
        <Switch>
          <Route exact path="/admin/auth/login" component={Login}/>
          <Route component={Admin} />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default withStore(App);
