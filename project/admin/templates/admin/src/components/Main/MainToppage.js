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

import Util from '../../common/util';

class MainToppage extends React.Component {
  state = {
    toppageData: []
  }

  tables=()=>{
    const self = this;
    Util.getAPI('/admin/api/models')
    .then(response=>{
      self.setState({toppageData: response.data});
    })
  }

  componentDidMount(){
    this.tables();
  }
  render() {
    const { classes } = this.props;
    let env = [];
    let pkg = [];

    console.log(this.state.toppageData);
    if(this.state.toppageData){

      for(let key in this.state.toppageData.env){
        let value = this.state.toppageData.env[key];
        env.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              {this.state.toppageData.env? value: ''}
            </TableCell>
          </TableRow>
        );
      }

      for(let key in this.state.toppageData.pkg){
        let value = this.state.toppageData.pkg[key];
        pkg.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              {this.state.toppageData.env? value: ''}
            </TableCell>
          </TableRow>
        );
      }
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
                    {env}
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