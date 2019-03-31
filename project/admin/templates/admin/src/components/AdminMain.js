import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import {Switch, Route, Redirect} from 'react-router-dom';
import MainToppage from './Main/MainToppage';

class AdminMain extends React.Component {
  render(){
    const { classes } = this.props;

    return(
      <div className={classes.main}>
        <Switch>
          <Route exact path="/admin" component={MainToppage} />
        </Switch>
      </div>
    );
  }
}

const styles = {
  main: {
    padding: '20px 30px 30px'
  }
}

export default withStyles(styles)(AdminMain);