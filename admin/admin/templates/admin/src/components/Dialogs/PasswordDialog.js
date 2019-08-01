import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

const PasswordDialog=(props)=>{
  const openDialog=()=>{
    props.openDialog();
  }

  const clickOK=()=>{
    props.handleOkMethod();
  }

  return(
    <Dialog
      open={props.isOpen}
      onClose={openDialog}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title">{"Succeed your password reset"}</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          New Password: {props.new_password}
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={clickOK} color="primary" autoFocus>
          OK
        </Button>
      </DialogActions>
    </Dialog>
  );
}

const styles = {

}

export default withStyles(styles)(withStore(PasswordDialog));
