import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import Const from './common/const';
import AdminAppBar from './components/AdminAppBar';
import AdminMain from './components/AdminMain';
import AdminDrawer from './components/AdminDrawer';

import {withStore} from './common/store';
import Util from './common/util';

class App extends Component {

  // componentDidMount(){
  //   const store = this.props.store;
  //   Util.getAPI('/admin/api/models')
  //   .then(response=>{
  //     if(response.data){
  //       console.log(response.data);
  //       store.set('models')(response.data.models);
  //       store.set('toppageData')(response.data);
  //     }
  //   })
  // }

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
