import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from './store';

import { withRouter } from 'react-router';

const NotFound=(props)=>{
  const {classes} = props;
  return (
    <div className={classes.style}>
      <div className={classes.content}>
        <div className={classes.title}>
          404 Not Found
          </div>
      </div>
    </div>
  );
}

const styles = {
  style: {
    backgroundColor: '#fff',
    color: '#636b6f',
    fontFamily: 'Raleway, sans-serif',
    //fontFamily: 'Raleway',
    fontWeight: 100,
    height: '80vh',
    margin: 0,
    alignItems: 'center',
    display: 'flex',
    justifyContent: 'center',
    position: 'relative',
  },
  content: {
    textAlign: 'center'
  },
  title: {
    fontSize: '84px',
    marginBottom: '30px'
  }
}

export default withStyles(styles)(withRouter(withStore(NotFound)));