import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import {withStore} from './common/store';

import Login from './components/Auth/Login';
import Admin from './components/Admin';
import Auth from './components/Auth/Auth';

class App extends React.Component {

  render(){
    return(
      <BrowserRouter>
        <Switch>
          <Route exact path="/admin/login" component={Login}/>
          <Auth>
            <Switch>
              <Route component={Admin} />
            </Switch>
          </Auth>
        </Switch>
      </BrowserRouter>
    );
  }
}

export default withStore(App);
