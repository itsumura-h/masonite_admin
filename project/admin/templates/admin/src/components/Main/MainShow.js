import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Grid from '@material-ui/core/Grid';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';

import { withRouter } from 'react-router';
import {NavLink} from 'react-router-dom';

import List from '@material-ui/icons/List';
import Edit from '@material-ui/icons/Edit';
import Delete from '@material-ui/icons/Delete';

import Util from '../../common/util';

class MainShow extends React.PureComponent{
  state = {
    schema: [],
    showData: [],
    editUrl: window.location.href + '/edit',
  }

  getSchema=(model)=>{
    const self = this;
    Util.getAPI('/admin/api/schema/'+model)
    .then(response=>{
      self.setState({schema: response.data});
    });
  }

  getShow=(model, id)=>{
    const self = this;
    Util.getAPI('/admin/api/'+model+'/'+id)
    .then(response=>{
      self.setState({showData: response.data});
    });
  }

  delete=(event)=>{
    // URLパラメーター取得
    const model = this.props.match.params.model;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    const id = event.currentTarget.dataset.id;
    const url = '/admin/api/'+model+'/'+id+'/delete';

    Util.deleteAPI(url)
    .then(response=>{
      this.props.history.push('./');
    })
    .catch(err=>{
      console.error(err);
    })
  }

  componentDidMount(){
    // URLパラメーター取得
    const model = this.props.match.params.model;
    const id = this.props.match.params.id;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    if(model){
      this.getSchema(model);
      this.getShow(model, id);
    }
  }

  componentDidUpdate(nextProps){
    // URLパラメーター取得
    const model = this.props.match.params.model;
    const id = this.props.match.params.id;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    if(this.props !== nextProps && table){
      this.getSchema(model);
      this.getShow(model, id);
    }
  }

  render(){
    const { classes } = this.props;
    // URLパラメーター取得
    const model = this.props.match.params.model;
    const id = this.props.match.params.id;

    let i = 0;
    let html_shows = [];
    for(let key in this.state.showData){
      let show = this.state.showData[key];
      html_shows.push(
        <div key={i}>
          <Grid container>
            <Grid item xs={2}><label>{key}</label></Grid>
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
        <div className={classes.flex}>
          <p>show</p>
          <div className={classes.buttons}>
            <NavLink to='./'>
              <Button color="primary">
                <List/>list
              </Button>
            </NavLink>
            <NavLink to={`./${id}/edit`}>
              <Button color="primary">
                <Edit/>edit
              </Button>
            </NavLink>
            <Button color="primary" data-id={this.props.match.params.id} onClick={this.delete}>
              <Delete/>delete
            </Button>
            </div>
        </div>
        <div className={classes.scroll}>
          {html_shows}
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
  },
  flex: {
    display: 'flex'
  },
  buttons: {
    margin: '0 0 0 auto'
  }
}

export default withStyles(styles)(withRouter(withStore(MainShow)));