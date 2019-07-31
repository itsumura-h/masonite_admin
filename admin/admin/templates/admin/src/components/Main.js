import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import {Switch, Route} from 'react-router-dom';
import Toppage from './Toppage';
import ResourceIndex from './Resource/ResourceIndex';
import ResourceCreate from './Resource/ResourceCreate';
import ResourceEdit from './Resource/ResourceEdit';
import ResourceShow from './Resource/ResourceShow';

import AuthIndex from './Auth/AuthIndex';
import AuthCreate from './Auth/AuthCreate';
import AuthShow from './Auth/AuthShow';
import AuthEdit from './Auth/AuthEdit';
import MypageShow from './Mypage/MypageShow';
import MypageEdit from './Mypage/MypageEdit';

import NotFound from '../common/404';
import CONST from '../common/const';

const Main=(props)=>{
  const { classes } = props;

  return(
    <div className={classes.main}>
      <Switch>
        <Route exact path="/admin" component={Toppage} />
        <Route exact path="/admin/auth" component={AuthIndex} />
        <Route exact path="/admin/auth/mypage" component={MypageShow} />
        <Route exact path="/admin/auth/mypage/edit" component={MypageEdit} />
        <Route exact path="/admin/auth" component={AuthIndex} />
        <Route exact path="/admin/auth/create" component={AuthCreate} />
        <Route exact path="/admin/auth/:id" component={AuthShow} />
        <Route exact path="/admin/auth/:id/edit" component={AuthEdit} />
        <Route exact path="/admin/:model" component={ResourceIndex} />
        <Route exact path="/admin/:model/create" component={ResourceCreate} />
        <Route exact path="/admin/:model/:id" component={ResourceShow} />
        <Route exact path="/admin/:model/:id/edit" component={ResourceEdit} />
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

export default withStyles(styles)(Main);