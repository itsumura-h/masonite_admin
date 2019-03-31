import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import {Link, NavLink} from 'react-router-dom';

import { withStore } from '../common/store'

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
};

class AdminAppBar extends React.Component {

  render(){
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <AppBar position="static">
          <Toolbar>
              <Typography variant="h6" color="inherit" className={classes.grow}>
              <NavLink to="/admin" style={{color: "yellow"}}>
                Masonite 管理サイト
                </NavLink>
              </Typography>
            <div>
              <span>ようこそname</span>
              <span> / </span>
              <NavLink to="/" style={{color: "white"}}>
                サイトを表示
              </NavLink>
              <span> / </span>
              <NavLink to="/admin" style={{color: "white"}}>
                パスワードの変更
              </NavLink>
              <span> / </span>
              <NavLink to="/admin" style={{color: "white"}}>
                ログアウト
              </NavLink>
            </div>
          </Toolbar>
        </AppBar>
      </div>
    );
  }
}

AdminAppBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(withStore(AdminAppBar));