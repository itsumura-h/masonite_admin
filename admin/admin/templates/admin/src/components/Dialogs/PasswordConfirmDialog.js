import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

const PasswordConfirmDialog=(props)=>{
  const openDialog=()=>{
    props.openDialog();
  }

  const clickOK=()=>{
    props.openDialog();
    props.handleOkMethod();
  }

  return(
    <Dialog
      open={props.isOpen}
      onClose={openDialog}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title">{"Do you want to delete?"}</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          Are you sure you wish to reset? This action cannot be undone.
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={openDialog}>
          Cancel
        </Button>
        <Button onClick={clickOK} data-id={props.id} color="primary" autoFocus>
          Reset
        </Button>
      </DialogActions>
    </Dialog>
  );
}

const styles = {

}

export default withStyles(styles)(withStore(PasswordConfirmDialog));