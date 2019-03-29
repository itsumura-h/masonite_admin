import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import Const from './common/const';
import AdminAppBar from './components/AdminAppBar';
import AdminDrawer from './components/AdminDrawer';
import AdminMain from './components/AdminMain';

import {withStore} from './common/store';

class App extends Component {

  render() {
    return (
      <BrowserRouter>
        <div className="App">
        <AdminDrawer/>
          <div className='rightContents' style={{marginLeft: this.props.store.state.drawerWidth}}>
            <AdminAppBar/>
            <AdminMain/>
          </div>
        </div>
      </BrowserRouter>
    );
  }
}

export default withStore(App);
