import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import Add from '@material-ui/icons/Add';
import Create from '@material-ui/icons/Create';

import {Link, NavLink} from 'react-router-dom';

import axios from 'axios';

class MainToppage extends React.Component {
  state = {
    toppageData: []
  }

  tables=()=>{
    const self = this;
    axios.get('http://localhost:8000/admin/api/tables')
    .then(response=>{
      if(response.headers['content-type'] == 'application/json; charset=utf-8'){
        self.setState({toppageData: response.data});
      }
    })
  }

  componentDidMount(){
    this.tables();
  }
  render() {
    const { classes } = this.props;

    let pkg = []
    for(let key in this.state.toppageData.pkg){
      let value = this.state.toppageData.pkg[key];

      pkg.push(
        <TableRow>
          <TableCell>
            {key}
          </TableCell>
          <TableCell>
            {this.state.toppageData.env? value: ''}
          </TableCell>
        </TableRow>
      );
    }

    return (
      <div>
        <h2>Dashboard</h2>
        <Grid container spacing={24}>
          <Grid item xs>
            <Card>
              <CardContent>
                Environment
                <Table>
                  <TableBody>
                    <TableRow>
                      <TableCell>
                        Python version
                      </TableCell>
                      <TableCell>
                        {this.state.toppageData.env? this.state.toppageData.env.Python_version: ''}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>
                        App name
                      </TableCell>
                      <TableCell>
                        {this.state.toppageData.env? this.state.toppageData.env.APP_NAME: ''}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>
                        CGI
                      </TableCell>
                      <TableCell>
                        {this.state.toppageData.env? this.state.toppageData.env.CGI: ''}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>
                        Uname
                      </TableCell>
                      <TableCell>
                        {this.state.toppageData.env? this.state.toppageData.env.Uname: ''}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>
                        Server
                      </TableCell>
                      <TableCell>
                        {this.state.toppageData.env? this.state.toppageData.env.Server: ''}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>
                       Locale
                      </TableCell>
                      <TableCell>
                        {this.state.toppageData.env? this.state.toppageData.env.Locale: ''}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>
                        Env
                      </TableCell>
                      <TableCell>
                        {this.state.toppageData.env? this.state.toppageData.env.Env: ''}
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs>
            <Card>
              <CardContent>
                Dependencies
                <Table>
                  <TableBody>
                    {pkg}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </div>
    );
  }
}

const styles = {
  table: {
    width: '60vw'
  },
  link: {
    color: 'gray',
    fontWeight: 'bolder'
  },
  title: {
    margin: '0 auto'
  }
}

export default withStyles(styles)(MainToppage);