import React from 'react';
import { withStyles } from '@material-ui/core/styles';

import Util from '../../common/util';

const styles = {

}

class MainEdit extends React.Component{
  state = {
    schema: []
  }

  getSchema=()=>{
    // get URL param
    const model = this.props.match.params.model;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    const self = this;
    // axios.get('http://localhost:8000/admin/api/schema/'+ table)
    // .then(response=>{
    //   if(response.headers['content-type'] === 'application/json; charset=utf-8'){
    //     self.setState({schema: response.data});
    //   }
    // })
    Util.getAPI('/admin/api/schema/'+ table)
    .then(response=>{
      self.setState({schema: response.data});
    })
  }

  render(){
    const { classes } = this.props;
    // get URL param
    const model = this.props.match.params.model;

    return(
      <div>
        <h1>{model}</h1>
        <p>edit</p>
      </div>
    );
  }
}

export default withStyles(styles)(MainEdit);