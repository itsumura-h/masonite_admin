import React, {Component} from 'react';
import AppBar from './AppBar';
import Main from './Main';
import Drawer from './Drawer';

import {withStore} from '../common/store';
import Util from '../common/util';

class Admin extends Component {
  getInfo=()=>{
    Util.getApi('/admin/api/info')
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
        <AppBar/>
        <Drawer/>
        <div className='rightContents' style={{marginLeft: store.get('drawerWidth')}}>
          <Main/>
        </div>
      </div>
    );
  }
}

export default withStore(Admin);
