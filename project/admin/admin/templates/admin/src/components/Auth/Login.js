import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import { withRouter } from 'react-router';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import TextField from '@material-ui/core/TextField';
import InputAdornment from '@material-ui/core/InputAdornment';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';

import Email from '@material-ui/icons/Email';
import Lock from '@material-ui/icons/Lock';

import Util from '../../common/util';

class Login extends React.Component {
  state = {
    params: [],
  }

  setParam=(event)=>{
    let new_params = this.state.params;
    const key = event.currentTarget.name;
    new_params[key] = event.currentTarget.value;
    console.log(new_params);
    this.setState({showData: new_params});
  }

  submit=()=>{
    const url = '/admin/api/login'
    Util.postAPI(url, this.state.params)
    .then(response=>{
      console.log(response);
      if(response.data.login === true){
        this.props.history.push('/admin');
      }
    })
    .catch(err=>{
      console.error(err);
    })
  }

  render(){
    const { classes } = this.props;

    return(
      <div className={classes.background}>
        <div className={classes.form}>
          <h1 className={classes.title}>Masonite Admin</h1>
          <Card>
            <CardContent>
              <TextField
                onChange={this.setParam}
                label="email"
                name="email"
                className={classes.textField}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <Email />
                    </InputAdornment>
                  ),
                }}
              />
              <TextField
                onChange={this.setParam}
                label="password"
                name="password"
                className={classes.textField}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <Lock />
                    </InputAdornment>
                  ),
                }}
                type="password"
              />
              <Divider />
              <div className={classes.flex}>
                <Button
                  variant="contained"
                  className={classes.saveButton}
                  data-id={this.props.match.params.id}
                  onClick={this.submit}
                >
                  Login
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }
}

const styles = {
  background: {
    backgroundColor: '#D2D6DE',
    minHeight: '100vh',
  },
  form: {
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    margin: 'auto',
    width: '50vw',
    height: '60vh'
  },
  title: {
    textAlign: 'center',
    color: '#444444'
  },
  textField: {
    width: '100%'
  },
  flex: {
    display: 'flex'
  },
  signUpButton: {
    color: 'black',
    backgroundColor: 'white',
    '&:hover': {
      backgroundColor: '#EEEEEE',
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

export default withStyles(styles)(withRouter(withStore(Login)));
