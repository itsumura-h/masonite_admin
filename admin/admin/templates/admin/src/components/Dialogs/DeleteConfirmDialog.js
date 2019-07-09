import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

const DeleteConfirmDialog=(props)=>{
  const openDelete=()=>{
    props.openDelete();
  }

  const clickOK=()=>{
    props.openDelete();
    props.handleOkMethod();
  }

  return(
    <Dialog
      open={props.isOpen}
      onClose={openDelete}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title">{"Do you want to delete?"}</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          Are you sure you wish to delete? This action cannot be undone.
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={openDelete}>
          Cancel
        </Button>
        <Button onClick={clickOK} data-id={props.id} color="primary" autoFocus>
          Delete
        </Button>
      </DialogActions>
    </Dialog>
  );
}

const styles = {

}

export default withStyles(styles)(withStore(DeleteConfirmDialog));