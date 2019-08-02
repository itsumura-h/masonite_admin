import React, { PureComponent } from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import { withRouter } from 'react-router';
import { NavLink } from 'react-router-dom';

import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import TextField from '@material-ui/core/TextField';

import List from '@material-ui/icons/List';
import Edit from '@material-ui/icons/Edit';
import Delete from '@material-ui/icons/Delete';

import Util from '../../common/util';
import DeleteConfirmDialog from '../Dialogs/DeleteConfirmDialog';

class AuthShow extends PureComponent{
  state = {
    showData: {},
    isOpenDeleteConfirm: false,
    targetId: 0,
  }

  //========================== API Access ==========================
  getShow=(id)=>{
    const self = this;
    Util.getApi(`/admin/api/auth/${id}`)
    .then(response=>{
      self.setState({showData: response.data});
    });
  }

  //========================== Delete ==========================
  openDialog=(event)=>{
    if(event){
      this.setState({targetId: event.currentTarget.dataset.id});
    }

    const newIsOpenDelete = this.state.isOpenDeleteConfirm? false: true;
    this.setState({isOpenDeleteConfirm: newIsOpenDelete});
  }

  delete=(event)=>{
    const id = this.state.targetId;
    const url = `/admin/api/auth/${id}/delete`;

    Util.deleteApi(url)
    .then(response=>{
      this.props.history.push('./');
    })
    .catch(err=>{
      console.error(err);
    })
  }

  //========================== React ==========================
  componentDidMount(){
    const id = this.props.match.params.id;
    this.getShow(id);
  }

  render(){
    const { classes } = this.props;
    const id = this.props.match.params.id;
    return (
      <div>
        <h1>Admin Users</h1>
        <Card>
          <CardContent>
            <div className={classes.flex}>
              <p>Detail</p>
              <div className={classes.buttons}>
                <NavLink to='./'>
                  <Button variant="contained" className={classes.listButton}>
                    <List/>list
                  </Button>
                </NavLink>
                <NavLink to={`./${id}/edit`}>
                  <Button variant="contained" className={classes.editButton}>
                    <Edit/>edit
                  </Button>
                </NavLink>
                <Button
                  onClick={this.openDialog}
                  data-id={this.props.match.params.id}
                  variant="contained"
                  className={classes.deleteButton}
                >
                  <Delete/>delete
                </Button>
              </div>
            </div>
            <Divider />
            <div className={classes.scroll}>
              <Table>
                <TableBody>
                  {
                    this.state.showData &&
                    Object.keys(this.state.showData).map((key, i)=>{
                      return(
                        <TableRow key={i}>
                          <TableCell>
                            {key}
                          </TableCell>
                          <TableCell>
                            <TextField
                              value={this.state.showData[key]}
                              InputProps={{
                                readOnly: true,
                              }}
                              multiline
                              className={classes.textarea}
                            />
                          </TableCell>
                        </TableRow>
                      );
                    })
                  }
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
        <DeleteConfirmDialog
          isOpen={this.state.isOpenDeleteConfirm}
          id={this.state.targetId}
          openDialog={this.openDialog}
          handleOkMethod={this.delete}
        />
    </div>
    );
  }
}

const styles = {
  scroll: {
    overflow: 'auto'
  },
  textarea: {
    width: '90%'
  },
  flex: {
    display: 'flex'
  },
  buttons: {
    margin: '0 0 0 auto'
  },
  listButton: {
    color: 'black',
    backgroundColor: '#ECF0F5'
  },
  editButton: {
    color: 'white',
    backgroundColor: '#3C8DBC',
    '&:hover': {
      backgroundColor: '#2C7DAC',
    },
  },
  deleteButton: {
    color: 'white',
    backgroundColor: '#DD4B39',
    '&:hover': {
      backgroundColor: '#CD3B29',
    },
  }
}

export default withStyles(styles)(withRouter(withStore(AuthShow)));