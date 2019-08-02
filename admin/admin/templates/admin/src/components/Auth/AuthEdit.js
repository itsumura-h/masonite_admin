import React, {PureComponent} from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import { withRouter } from 'react-router';
import {NavLink} from 'react-router-dom';

import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import TextField from '@material-ui/core/TextField';

import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

import List from '@material-ui/icons/List';
import Save from '@material-ui/icons/Save';
import Delete from '@material-ui/icons/Delete';

import Util from '../../common/util';
import DeleteConfirmDialog from '../Dialogs/DeleteConfirmDialog';
import PasswordDialog from '../Dialogs/PasswordDialog';

class AuthEdit extends PureComponent{
  state = {
    showData: {},
    params: {},
    error: '',
    isOpenDeleteConfirm: false,
    targetId: 0,
    isOpenPasswordDialog: false,
    new_password: '',
  }

  //========================== API Access ==========================
  getShow=()=>{
    const self = this;
    const id = this.props.match.params.id;
    Util.getApi(`/admin/api/auth/${id}`)
    .then(response=>{
      self.setState({showData: response.data});
    });
  }

  //========================== Save ==========================
  setParam=(event)=>{
    let new_params = this.state.params;
    const key = event.currentTarget.name;
    new_params[key] = event.currentTarget.value;
    this.setState({params: new_params});
    this.forceUpdate();
  }

  save=(event)=>{
    const id = event.currentTarget.dataset.id;
    const url = `/admin/api/auth/${id}/update`;

    Util.putApi(url, this.state.params)
    .then(response=>{
      if(!response.data.error){
        this.props.history.push(`../${id}`);
      }else{
        this.setState({error: response.data.error});
      }
    })
    .catch(err=>{
      console.log(err);
    })
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
      this.props.history.push('../');
    })
    .catch(err=>{
      console.error(err);
    })
  }

  //========================== Password Reset ==========================
  passwordReset=(event)=>{
    const id = this.state.showData.id
    const url = `/admin/api/auth/${id}/reset_password`;

    Util.postApi(url, {})
    .then(response=>{
      this.setState({new_password: response.data.new_password});
      this.openPasswordDialog()
    })
    .catch(err=>{
      console.error(err);
    })
  }

  openPasswordDialog=()=>{
    const newIsOpenPasswordDialog = this.state.isOpenPasswordDialog? false: true;
    this.setState({isOpenPasswordDialog: newIsOpenPasswordDialog});
  }

  passwordResetOK=()=>{
    this.openPasswordDialog()
    const id = this.props.match.params.id;
    this.props.history.push(`/admin/auth/${id}`);
  }

  //========================== React ==========================
  componentDidMount(){
    this.getShow()
  }

  render(){
    const { classes, store } = this.props;
    return(
      <div>
        <h1>Admin Users</h1>
        <p className={classes.error}>{this.state.error}</p>
        <Card>
          <CardContent>
            <div className={classes.flex}>
              <p>Edit</p>
              <div className={classes.buttons}>
                <NavLink to='../'>
                  <Button variant="contained" className={classes.listButton}>
                    <List/>list
                  </Button>
                </NavLink>
                <Button variant="contained"
                  className={classes.saveButton}
                  data-id={this.props.match.params.id}
                  onClick={this.save}
                  disabled={Object.keys(this.state.params).length === 0? true: false}
                >
                  <Save/>save
                </Button>
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
                  <TableRow key={1}>
                    <TableCell>
                      ID
                    </TableCell>
                    <TableCell>
                      <TextField
                        value={this.state.showData.id}
                        name='id'
                        multiline
                        className={classes.textarea + ' params'}
                        InputProps={{
                          readOnly: true,
                        }}
                      />
                    </TableCell>
                  </TableRow>
                  <TableRow key={2}>
                    <TableCell>
                      name
                    </TableCell>
                    <TableCell>
                      {
                        Object.keys(this.state.showData).length > 0 &&
                        <TextField
                          defaultValue={this.state.showData.name}
                          onChange={this.setParam}
                          name='name'
                          multiline
                          className={classes.textarea + ' params'}
                        />
                      }
                    </TableCell>
                  </TableRow>
                  <TableRow key={3}>
                    <TableCell>
                      email
                    </TableCell>
                    <TableCell>
                      {
                        Object.keys(this.state.showData).length > 0 &&
                        <TextField
                          defaultValue={this.state.showData.email}
                          onChange={this.setParam}
                          name='email'
                          multiline
                          className={classes.textarea + ' params'}
                        />
                      }
                    </TableCell>
                  </TableRow>
                  <TableRow key={4}>
                    <TableCell>
                    permission
                    </TableCell>
                    <TableCell>
                      <FormControl fullWidth className={classes.formControl}>
                        {
                          Object.keys(this.state.showData).length > 0 &&
                          <Select
                            defaultValue={this.state.showData.permission}
                            onChange={this.setParam}
                            name='permission'
                            className='params'
                            autoWidth
                            native
                          >
                            <option key={0} value="administrator">administrator</option>
                            <option key={1} value="member">member</option>
                            <option key={2} value="user">user</option>
                          </Select>
                        }
                      </FormControl>
                    </TableCell>
                  </TableRow>
                  <TableRow key={5}>
                    <TableCell>
                      password reset
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="contained"
                        className={classes.listButton}
                        onClick={this.passwordReset}
                      >
                        Reset
                      </Button>
                    </TableCell>
                  </TableRow>
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
        <PasswordDialog
          isOpen={this.state.isOpenPasswordDialog}
          new_password={this.state.new_password}
          handleOkMethod={this.passwordResetOK}
        />
    </div>
    );
  }
}

const styles = {
  scroll: {
    overflow: 'auto'
  },
  error: {
    backgroundColor: 'yellow'
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
  saveButton: {
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

export default withStyles(styles)(withRouter(withStore(AuthEdit)));