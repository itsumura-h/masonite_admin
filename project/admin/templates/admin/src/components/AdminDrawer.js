import React from 'react';
import PropTypes from 'prop-types';
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

import { withStyles } from '@material-ui/core/styles';

import { withStore } from '../common/store'

class AdminDrawer extends React.Component {
  state = {
    tables: null,
  }

  componentDidMount(){
    const store = this.props.store;
    Util.getAPI('/admin/api/models')
    .then(response=>{
      if(response.data){
        store.set('models')(response.data.models);
      }
    })
  }

  render() {
    const { classes, theme } = this.props;
    const state = this.props.store.state;

    let tables = [];
    if(state.models){
      for(let i in state.models){
        let model = state.models[i]
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
        onClose={this.handleDrawerToggle}
        classes={{
          paper: classes.drawerPaper,
        }}
      >
        <List>
          {tables}
        </List>
      </Drawer>
    );
  }
}

const styles = theme => ({
  drawer: {
    [theme.breakpoints.up('sm')]: {
      width: 240,
      flexShrink: 0,
    },
  },
  drawerPaper: {
    width: 240,
  },
});

export default withStyles(styles, { withTheme: true })(withStore(AdminDrawer));