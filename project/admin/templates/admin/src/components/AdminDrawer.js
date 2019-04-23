import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../common/store'

import AppBar from '@material-ui/core/AppBar';
import CssBaseline from '@material-ui/core/CssBaseline';
import Divider from '@material-ui/core/Divider';
import Drawer from '@material-ui/core/Drawer';
import Hidden from '@material-ui/core/Hidden';
import IconButton from '@material-ui/core/IconButton';
import InboxIcon from '@material-ui/icons/MoveToInbox';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import MailIcon from '@material-ui/icons/Mail';
import MenuIcon from '@material-ui/icons/Menu';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

import {Link} from 'react-router-dom';

import Util from '../common/util';



class AdminDrawer extends React.Component {
  state = {
    tables: null,
  }

  render() {
    const { classes, theme } = this.props;
    const state = this.props.store.state;

    let tables = [];
    if(state.info.models){
      for(let i in state.info.models){
        let model = state.info.models[i]
        tables.push(
          <Link to={"/admin/"+model} key={i}>
            <ListItem button>
              <ListItemText primary={model + ' Management'} />
            </ListItem>
          </Link>
        );
        i++;
      }
    }

    return (
      <Drawer
        container={this.props.container}
        variant="persistent"
        anchor="left"
        open={state.drawerOpen}
        classes={{
          paper: classes.drawerPaper,
        }}
      >
        <List className={classes.modelList}>
          {tables}
        </List>
      </Drawer>
    );
  }
}

const styles = {
  drawerPaper: {
    width: 240,
    backgroundColor: '#F9FAFC'
  },
  modelList: {
    backgroundColor: '#F4F4F5'
  }
}

export default withStyles(styles)(withStore(AdminDrawer));