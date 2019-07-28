import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import {Switch, Route} from 'react-router-dom';
import MainToppage from './Main/MainToppage';
import MainIndex from './Main/MainIndex';
import MainCreate from './Main/MainCreate';
import MainEdit from './Main/MainEdit';
import MainShow from './Main/MainShow';

import ManageAdminUserIndex from './ManageAdminUser/ManageAdminUserIndex';
import ManageAdminUserShow from './ManageAdminUser/ManageAdminUserShow';
import ManageAdminUserEdit from './ManageAdminUser/ManageAdminUserEdit';

import NotFound from '../common/404';
import CONST from '../common/const';

const AdminMain=(props)=>{
  const { classes } = props;

  return(
    <div className={classes.main}>
      <Switch>
        <Route exact path="/admin" component={MainToppage} />
        <Route exact path="/admin/ManageAdminUser" component={ManageAdminUserIndex} />
        <Route exact path="/admin/ManageAdminUser/:id" component={ManageAdminUserShow} />
        <Route exact path="/admin/ManageAdminUser/:id/edit" component={ManageAdminUserEdit} />
        <Route exact path="/admin/:model" component={MainIndex} />
        <Route exact path="/admin/:model/create" component={MainCreate} />
        <Route exact path="/admin/:model/:id" component={MainShow} />
        <Route exact path="/admin/:model/:id/edit" component={MainEdit} />
        <Route component={NotFound} />
      </Switch>
    </div>
  );
}

const styles = {
  main: {
    marginTop: `${CONST.appBarHeight}px`,
    padding: '20px 30px 30px',
    backgroundColor: '#ECF0F5',
    minHeight: '80vh',
  }
}

export default withStyles(styles)(AdminMain);