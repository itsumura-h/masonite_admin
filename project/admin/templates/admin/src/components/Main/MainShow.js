import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Util from '../../common/util';

class MainShow extends React.PureComponent{
  state = {
    schema: [],
    show: [],
  }

  getSchema=(table)=>{
    const self = this;
    Util.getAPI('/admin/api/schema/'+table)
    .then(response=>{
      self.setState({schema: response.data});
    });
  }

  getShow=(table, id)=>{
    const self = this;
    Util.getAPI('/admin/api/'+table+'/'+id)
    .then(response=>{
      self.setState({show: response.data});
    });
  }

  componentDidMount(){
    // URLパラメーター取得
    const model = this.props.match.params.model;
    const id = this.props.match.params.id;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    if(table){
      this.getSchema(table);
      this.getShow(table, id);
    }
  }

  componentDidUpdate(nextProps){
    // URLパラメーター取得
    const model = this.props.match.params.model;
    const id = this.props.match.params.id;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    if(this.props !== nextProps && table){
      this.getSchema(table);
      this.getShow(table, id);
    }
  }

  render(){
    console.log(this.state.schema);
    console.log(this.state.show);
    const { classes } = this.props;
    // URLパラメーター取得
    const model = this.props.match.params.model;

    return(
      <div>
        <h1>{model}</h1>
        <p>show</p>
        <div className={classes.scroll}>
        </div>
      </div>
    );
  }
}

const styles = {
  scroll: {
    overflow: 'auto'
  }
}

export default withStyles(styles)(withStore(MainShow));