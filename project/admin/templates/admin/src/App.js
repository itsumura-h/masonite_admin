import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';
import './App.css';
import AdminAppBar from './components/AdminAppBar';
import AdminMain from './components/AdminMain';
import AdminDrawer from './components/AdminDrawer';

import {withStore} from './common/store';
import Util from './common/util';

class App extends Component {

  getInfo=()=>{
    const store = this.props.store;
    Util.getAPI('/admin/api/info')
    .then(response=>{
      if(response.data){
        store.set('info')(response.data);
      }
    })
  }

  componentDidMount(){
    this.getInfo();
  }

  render() {
    return (
      <BrowserRouter>
        <AdminDrawer/>
          <div className='rightContents' style={{marginLeft: this.props.store.state.drawerWidth}}>
            <AdminAppBar/>
            <AdminMain/>
          </div>
      </BrowserRouter>
    );
  }
}

export default withStore(App);
