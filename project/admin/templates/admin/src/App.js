import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import {withStore} from './common/store';

import SignIn from './components/Login/SignIn';
import Admin from './components/Admin';

class App extends React.Component {

  render(){
    return(
      <BrowserRouter>
        <Switch>
          <Route exact path="/admin/login" component={SignIn}/>
          <Route component={Admin} />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default withStore(App);
