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

import Util from '../../common/util';
import CreateAdminDialog from '../Dialogs/CreateAdminDialog';


class AuthCreate extends PureComponent {
  state = {
    schema: [],
    foreignKeys: [],
    params: {'name': '', 'email': '', 'permission': 'administrator'},
    error: '',
    isOpenCreateAdminDialog: false,
    password: '',
  }

  //========================== Save ==========================
  setParam=(event)=>{
    let new_params = this.state.params;
    const key = event.currentTarget.name;
    new_params[key] = event.currentTarget.value;
    this.setState({params: new_params});
    this.forceUpdate();
  }

  save=()=>{
    const url = '/admin/api/auth'
    Util.postApi(url, this.state.params)
    .then(response=>{
      if(!response.data.error){
        this.setState({password: response.data.password});
        this.OpenCreateAdminDialog()
      }else{
        this.setState({error: response.data.error});
      }
    })
    .catch(err=>{
      console.log(err);
    })
  }

  OpenCreateAdminDialog=()=>{
    const newIsOpenCreateAdminDialog =
      this.state.isOpenCreateAdminDialog? false: true;
    this.setState({isOpenCreateAdminDialog: newIsOpenCreateAdminDialog});
  }

  createAdminOK=()=>{
    this.OpenCreateAdminDialog()
    this.props.history.push(`/admin/auth`);
  }

  //========================== React ==========================
  render(){
    const { classes, store } = this.props;
    return(
      <div>
        <h1>Admin Users</h1>
        <p className={classes.error}>{this.state.error}</p>
        <Card>
          <CardContent>
            <div className={classes.flex}>
              <p>create</p>
              <div className={classes.buttons}>
                <NavLink to='./'>
                  <Button variant="contained" className={classes.listButton}>
                    <List/>list
                  </Button>
                </NavLink>
              </div>
            </div>
            <Divider />
            <div className={classes.scroll}>
              <Table>
                <TableBody>
                  <TableRow key={0}>
                    <TableCell>
                      name
                    </TableCell>
                    <TableCell>
                      <TextField
                        onChange={this.setParam}
                        name='name'
                        multiline
                        className={classes.textarea + ' params'}
                      />
                    </TableCell>
                  </TableRow>
                  <TableRow key={1}>
                    <TableCell>
                      email
                    </TableCell>
                    <TableCell>
                      <TextField
                        onChange={this.setParam}
                        name='email'
                        multiline
                        className={classes.textarea + ' params'}
                      />
                    </TableCell>
                  </TableRow>
                  <TableRow key={2}>
                    <TableCell>
                      permission
                    </TableCell>
                    <TableCell>
                      <FormControl fullWidth className={classes.formControl}>
                        <Select
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
                      </FormControl>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </div>
            <Divider />
            <div className={classes.flex}>
              <Button variant="contained" className={classes.saveButton} data-id={this.props.match.params.id} onClick={this.save}>
                <Save/>save
              </Button>
            </div>
          </CardContent>
        </Card>
        <CreateAdminDialog
          isOpen={this.state.isOpenCreateAdminDialog}
          password={this.state.password}
          handleOkMethod={this.createAdminOK}
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
  resetButton: {
    color: 'white',
    backgroundColor: '#F39C12',
    '&:hover': {
      backgroundColor: '#E38C02',
    },
  },
  saveButton: {
    margin: '0 0 0 auto',
    color: 'white',
    backgroundColor: '#3C8DBC',
    '&:hover': {
      backgroundColor: '#2C7DAC',
    },
  },
}

export default withStyles(styles)(withRouter(withStore(AuthCreate)));
