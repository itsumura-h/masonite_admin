import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../common/store'
import { withRouter } from 'react-router-dom'

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import {NavLink} from 'react-router-dom';
import Util from '../common/util';

class AdminAppBar extends React.Component {

  drawerOpen=()=>{
    const store = this.props.store;
    const newIsOpen = store.get('drawerOpen')? false: true;
    store.set('drawerOpen')(newIsOpen);
    const newWidth = store.get('drawerWidth') === 240? 0: 240;
    store.set('drawerWidth')(newWidth);
  }

  logout=()=>{
    Util.logoutApi()
    .then(response=>{
      window.localStorage.removeItem('login_id');
      window.localStorage.removeItem('login_token');
      window.localStorage.removeItem('login_name');
      this.props.history.push('/admin/login')
    })
    .catch(err=>{
      console.error(err);
    })
  }

  render(){
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <AppBar position="static" className={classes.appbar}>
          <Toolbar>
            <IconButton onClick={this.drawerOpen} className={classes.menuButton} color="inherit" aria-label="Menu">
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" color="inherit" className={classes.grow}>
              <NavLink to="/admin" className={classes.link}>
                Masonite Admin
              </NavLink>
            </Typography>
            <Typography variant="h6" color="inherit">
              Welcome! <span className={classes.loginName}>{window.localStorage.getItem('login_name')}</span>
            </Typography>
            <Button color="inherit" onClick={this.logout} className={classes.logoutButton} >Log Out</Button>
          </Toolbar>
        </AppBar>
      </div>
    );
  }
}

const styles = {
  root: {
    flexGrow: 1,
  },
  grow: {
    flexGrow: 1,
  },
  loginName: {
    color: 'yellow',
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
  link: {
    color: 'white'
  },
  appbar: {
    backgroundColor: '#3C8DBC'
  },
  logoutButton: {
    backgroundColor: '#EEEEEE',
    color: '#000000',
    '&:hover': {
      backgroundColor: '#DDDDDD',
    },
    marginLeft: '10px',
  }
};

export default withStyles(styles)(withRouter(withStore(AdminAppBar)));