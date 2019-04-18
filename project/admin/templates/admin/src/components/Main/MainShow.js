import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Grid from '@material-ui/core/Grid';
import Divider from '@material-ui/core/Divider';

import Util from '../../common/util';

class MainShow extends React.PureComponent{
  state = {
    //schema: [],
    show: [],
  }

  // getSchema=(table)=>{
  //   const self = this;
  //   Util.getAPI('/admin/api/schema/'+table)
  //   .then(response=>{
  //     self.setState({schema: response.data});
  //   });
  // }

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
      //this.getSchema(table);
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
      //this.getSchema(table);
      this.getShow(table, id);
    }
  }

  render(){
    console.log(this.state.show);
    const { classes } = this.props;
    // URLパラメーター取得
    const model = this.props.match.params.model;

    let i = 0;
    let shows = [];
    for(let key in this.state.show){
      let show = this.state.show[key];
      shows.push(
        <div key={i}>
          <Grid container>
            <Grid item xs='2'><label>{key}</label></Grid>
            <Grid item xs><textarea type='text' readOnly value={show} className={classes.textarea} /></Grid>
          </Grid>
          <Divider/>
        </div>
      );
      i++;
    }

    return(
      <div>
        <h1>{model}</h1>
        <p>show</p>
        <div className={classes.scroll}>
          {shows}
        </div>
      </div>
    );
  }
}

const styles = {
  scroll: {
    overflow: 'auto'
  },
  textarea: {
    width: '90%'
  }
}

export default withStyles(styles)(withStore(MainShow));