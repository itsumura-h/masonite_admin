import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';


class MainToppage extends React.Component {

  render() {
    const state = this.props.store.state;
    let env = [];
    let pkg = [];

    if(state.info){

      for(let key in state.info.env){
        let value = state.info.env[key];
        env.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              {state.info.env? value: ''}
            </TableCell>
          </TableRow>
        );
      }

      for(let key in state.info.pkg){
        let value = state.info.pkg[key];
        pkg.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              {state.info.env? value: ''}
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

export default withStyles(styles)(withStore(MainToppage));