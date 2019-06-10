import React from 'react';
import AdminAppBar from '../components/AdminAppBar';
import AdminMain from '../components/AdminMain';
import AdminDrawer from '../components/AdminDrawer';

import {withStore} from '../common/store';
import Util from '../common/util';

class Admin extends React.Component {
  getInfo=()=>{
    Util.getAPI('/admin/api/info')
    .then(response=>{
      this.props.store.set('info')(response.data);
    });
  }

  componentDidMount(){
    if(Object.keys(this.props.store.get('info')).length === 0){
      this.getInfo();
    }
  }

  render() {
    const {store} = this.props;

    return (
      <div>
        <AdminDrawer/>
        <div className='rightContents' style={{marginLeft: store.get('drawerWidth')}}>
          <AdminAppBar/>
          <AdminMain/>
        </div>
      </div>
    );
  }
}

export default withStore(Admin);