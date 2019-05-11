import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../common/store'

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import {NavLink} from 'react-router-dom';

class AdminAppBar extends React.Component {

  drawerOpen=()=>{
    const store = this.props.store;
    const newIsOpen = store.get('drawerOpen')? false: true;
    store.set('drawerOpen')(newIsOpen);
    const newWidth = store.get('drawerWidth') === 240? 0: 240;
    store.set('drawerWidth')(newWidth);
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
            <NavLink to='/admin/auth/login' className={classes.link}>
              <Button color="inherit">Log Out</Button>
            </NavLink>
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
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
  link: {
    color: 'white'
  },
  appbar: {
    backgroundColor: '#3C8DBC'
  }
};

export default withStyles(styles)(withStore(AdminAppBar));