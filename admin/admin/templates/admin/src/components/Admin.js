import React from 'react';
import AdminAppBar from '../components/AdminAppBar';
import AdminMain from '../components/AdminMain';
import AdminDrawer from '../components/AdminDrawer';

import {withStore} from '../common/store';
import Util from '../common/util';

class Admin extends React.Component {
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
    if(Object.keys(this.props.store.state.info).length === 0){
      this.getInfo();
    }
  }

  render() {
    return (
      <div>
        <AdminDrawer/>
        <div className='rightContents' style={{marginLeft: this.props.store.state.drawerWidth}}>
          <AdminAppBar/>
          <AdminMain/>
        </div>
      </div>
    );
  }
}

export default withStore(Admin);