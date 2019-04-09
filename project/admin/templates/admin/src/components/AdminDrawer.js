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

import Link from 'react-router-dom/Link';
import axios from 'axios';
import { withStyles } from '@material-ui/core/styles';

import { withStore } from '../common/store'

const styles = theme => ({
  // root: {
  //   display: 'flex',
  // },
  drawer: {
    [theme.breakpoints.up('sm')]: {
      width: 240,
      flexShrink: 0,
    },
  },
  drawerPaper: {
    width: 240,
  },
  // content: {
  //   flexGrow: 1,
  //   padding: theme.spacing.unit * 3,
  // },
});

class AdminDrawer extends React.Component {
  state = {
    tables: [],
  }

  componentDidMount(){
    const self = this;
    axios.get('http://localhost:8000/admin/api/tables')
    .then(function(response){
      if(response.headers['content-type'] == 'application/json; charset=utf-8'){
        self.setState({tables: response.data.tables});
      }
    })
  }

  render() {
    const { classes, theme } = this.props;
    let store = this.props.store;

    let tables = [];
    let i = 0;
    for(let table of this.state.tables){
      tables.push(
        <Link to={"/admin/"+table}>
          <ListItem button key={i}>
            <ListItemText primary={table} />
          </ListItem>
        </Link>
      );
      i++;
    }

    const drawer = (
      <div>
        <div className={classes.toolbar} />
        <List>
          {this.state.tables.map((table) => (
            <ListItem button key={table}>
              <ListItemIcon>{table % 2 === 0 ? <InboxIcon /> : <MailIcon />}</ListItemIcon>
              <ListItemText primary={table} />
            </ListItem>
          ))}
        </List>
      </div>
    );

    return (
      <Drawer
        container={this.props.container}
        variant="persistent"
        anchor="left"
        open={store.state.drawerOpen}
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

AdminDrawer.propTypes = {
  classes: PropTypes.object.isRequired,
  // Injected by the documentation to work in an iframe.
  // You won't need it on your project.
  container: PropTypes.object,
  theme: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(withStore(AdminDrawer)); 