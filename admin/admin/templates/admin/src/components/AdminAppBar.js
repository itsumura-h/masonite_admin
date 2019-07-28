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

const AdminAppBar=(props)=>{
  const { classes, store } = props;

  const drawerOpen=()=>{
    const newIsOpen = store.get('drawerOpen')? false: true;
    store.set('drawerOpen')(newIsOpen);
    const newWidth = store.get('drawerWidth') === 240? 0: 240;
    store.set('drawerWidth')(newWidth);
  }

  const logout=()=>{
    Util.logoutApi()
    .then(response=>{
      window.localStorage.removeItem('login_id');
      window.localStorage.removeItem('login_token');
      window.localStorage.removeItem('login_name');
      window.localStorage.removeItem('login_permission');
      props.history.push('/admin/login')
    })
    .catch(err=>{
      console.error(err);
    })
  }

  const clickUserEditButton=()=>{
    props.history.push('/admin/ManageAdminUser');
  }

  const UserEditButton=(props)=>{
    const login_permission = localStorage.getItem('login_permission');
    if(login_permission === 'administrator'){
      return <Button color="inherit" onClick={props.clickUserEditButton} className={props.classes.logoutButton}>user edit</Button>;
    }else{
      return null;
    }
  }

  return (
    <div className={classes.root}>
      <AppBar position="fixed" className={classes.appbar}>
        <Toolbar>
          <IconButton onClick={drawerOpen} className={classes.menuButton} color="inherit" aria-label="Menu">
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
            <UserEditButton clickUserEditButton={clickUserEditButton} classes={classes}/>
          <Button color="inherit" onClick={logout} className={classes.logoutButton} >Log Out</Button>
        </Toolbar>
      </AppBar>
    </div>
  );
}


const styles=(theme)=>({
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
    backgroundColor: '#3C8DBC',
    zIndex: theme.zIndex.drawer + 1,
  },
  logoutButton: {
    backgroundColor: '#EEEEEE',
    color: '#000000',
    '&:hover': {
      backgroundColor: '#DDDDDD',
    },
    marginLeft: '10px',
  }
});

export default withStyles(styles, true)(withRouter(withStore(AdminAppBar)));