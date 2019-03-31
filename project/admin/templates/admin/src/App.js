import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import Const from './common/const';
import AdminAppBar from './components/AdminAppBar';
import AdminMain from './components/AdminMain';

import {withStore} from './common/store';

class App extends Component {

  render() {
    return (
      <BrowserRouter>
        <div className="App">
          <AdminAppBar/>
          <AdminMain/>
        </div>
      </BrowserRouter>
    );
  }
}

export default withStore(App);
