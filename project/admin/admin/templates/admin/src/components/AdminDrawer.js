import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../common/store'

import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

import {Link} from 'react-router-dom';

class AdminDrawer extends React.Component {
  state = {
    tables: null,
  }

  render() {
    const { classes } = this.props;
    const state = this.props.store.state;

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
          {
            state.info.models &&
            state.info.models.map((model, i)=>{
              return (
                <Link to={"/admin/"+model['en']} key={i}>
                  <ListItem button>
                    <ListItemText primary={model['str']} />
                  </ListItem>
                </Link>
              );
            })
          }
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