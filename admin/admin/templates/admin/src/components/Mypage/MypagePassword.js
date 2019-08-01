import React, {PureComponent} from 'react';
import { withStyles } from '@material-ui/core/styles';
// import { withStore } from '../../common/store';

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

import List from '@material-ui/icons/List';
import Save from '@material-ui/icons/Save';

import PasswordDialog from '../Dialogs/PasswordDialog';
import Util from '../../common/util';

class MyapagePassword extends PureComponent {
  state = {
    params: {'password': '', 'new_password': ''},
    error: '',
    isOpenPasswordConfirm: false,
  }

  // ==================== Save ====================
  setParam=(event)=>{
    let new_params = this.state.params;
    const key = event.currentTarget.name;
    new_params[key] = event.currentTarget.value;
    this.setState({params: new_params});
    this.forceUpdate();
  }

  save=()=>{
    const url = `/admin/api/auth/mypage/update_password`;

    Util.putApi(url, this.state.params)
    .then(response=>{
      if(!response.data.error){
        this.props.history.push(`/admin/auth/mypage`);
      }else{
        this.setState({error: response.data.error});
      }
    })
    .catch(err=>{
      console.log(err);
    })
  }

  // ==================== React ====================

  render(){
    const { classes, store } = this.props;
    console.log(this.state.params)
    return(
      <div>
        <h1>Mypage</h1>
        <p className={classes.error}>{this.state.error}</p>
        <Card>
          <CardContent>
            <div className={classes.flex}>
              <p>Change Password</p>
              <div className={classes.buttons}>
                <NavLink to='./'>
                  <Button variant="contained" className={classes.listButton}>
                    <List/>Back
                  </Button>
                </NavLink>
              </div>
            </div>
            <Divider />
            <div className={classes.scroll}>
              <Table>
                <TableBody>
                  <TableRow key={1}>
                    <TableCell>
                      Password
                    </TableCell>
                    <TableCell>
                      <TextField
                        name='password'
                        type='password'
                        multiline
                        onChange={this.setParam}
                        className={classes.textarea + ' params'}
                      />
                    </TableCell>
                  </TableRow>
                  <TableRow key={2}>
                  <TableCell>
                      New Password
                    </TableCell>
                    <TableCell>
                      <TextField
                        name='new_password'
                        type='password'
                        multiline
                        onChange={this.setParam}
                        className={classes.textarea + ' params'}
                      />
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </div>
            <Divider/>
            <div className={classes.flex}>
              <Button variant="contained"
                className={classes.saveButton}
                onClick={this.save}
                disabled={Object.keys(this.state.params).length === 0? true: false}
              >
                <Save/>save
              </Button>
            </div>
          </CardContent>
        </Card>
        <PasswordDialog
          isOpen={this.state.isOpenPasswordConfirm}
          handleOkMethod={this.openDialog}
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
    backgroundColor: '#ECF0F5',
  },
  saveButton: {
    margin: '0 0 0 auto',
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
  },
  passwordButton: {
    color: 'black',
    backgroundColor: '#ECF0F5',
    margin: '10px'
  },
}

export default withStyles(styles)(withRouter(MyapagePassword));
