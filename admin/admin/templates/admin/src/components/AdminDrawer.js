import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../common/store'

import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

import {Link} from 'react-router-dom';

import CONST from '../common/const';

const AdminDrawer=(props)=>{
  const { classes, store } = props;

  return (
    <Drawer
      container={props.container}
      variant="persistent"
      anchor="left"
      open={store.get('drawerOpen')}
      classes={{
        paper: classes.drawerPaper,
      }}
    >
      <List className={classes.modelList}>
        <ListItem className={classes.title}>
          <ListItemText primary={'Table List'}/>
        </ListItem>
        {
          'models' in store.get('info') &&
          store.get('info').models.map((model, i)=>{
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

const styles = {
  title: {
    backgroundColor: '#F4F4F5'
  },
  drawerPaper: {
    width: 240,
  },
  modelList: {
    marginTop: `${CONST.appBarHeight}px`,
  }
}

export default withStyles(styles)(withStore(AdminDrawer));