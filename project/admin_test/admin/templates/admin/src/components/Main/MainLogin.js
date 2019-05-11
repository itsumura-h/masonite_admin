import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import { withRouter } from 'react-router';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import TextField from '@material-ui/core/TextField';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';


class Login extends React.Component {
  state = {

  }

  render(){
    const { classes } = this.props;

    return(
      <div>
        <h1>Login</h1>
        <Card>
          <CardContent>
            <Table>
              <TableBody>
                <TableRow key="name">
                  <TableCell>
                    name
                  </TableCell>
                  <TableCell>
                    <TextField
                      //onChange={this.setParam}
                      name="name"
                      className={classes.textarea + ' params'}
                    />
                  </TableCell>
                </TableRow>
                <TableRow key="email">
                  <TableCell>
                    email
                  </TableCell>
                  <TableCell>
                    <TextField
                      //onChange={this.setParam}
                      name="email"
                      className={classes.textarea + ' params'}
                    />
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
            <Divider />
            <div className={classes.flex}>
              <div className={classes.buttons}>
                <Button variant="contained" className={classes.saveButton} data-id={this.props.match.params.id} onClick={this.save}>
                  Login
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }
}

const styles = {
  textarea: {
    width: '90%'
  },
  flex: {
    display: 'flex'
  },
  buttons: {
    margin: '0 0 0 auto'
  },
  saveButton: {
    color: 'white',
    backgroundColor: '#3C8DBC',
    '&:hover': {
      backgroundColor: '#2C7DAC',
    },
  },
}

export default withStyles(styles)(withRouter(withStore(Login)));
