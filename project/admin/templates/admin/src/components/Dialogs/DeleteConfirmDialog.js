import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

class DeleteConfirmDialog extends React.Component {
  openDelete=()=>{
    this.props.openDelete();
  }

  clickOK=()=>{
    this.props.openDelete();
    this.props.handleOkMethod();
  }

  render(){
    return(
      <Dialog
          open={this.props.isOpen}
          onClose={this.openDelete}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">{"Do you want to delete this data?"}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              If you want to delete this data, click OK button
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.openDelete} color="secondly">
              Cancel
            </Button>
            <Button onClick={this.clickOK} data-id={this.props.id} color="primary" autoFocus>
              OK
            </Button>
          </DialogActions>
        </Dialog>
    );
  }
}

const styles = {

}

export default withStyles(styles)(withStore(DeleteConfirmDialog));