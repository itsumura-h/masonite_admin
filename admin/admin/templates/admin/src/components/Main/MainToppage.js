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
                    {
                      state.info.env && Object.keys(state.info.env).map((key, i)=>{
                        let value = state.info.env[key];
                        return (
                          <TableRow key={i}>
                            <TableCell>
                              {key}
                            </TableCell>
                            <TableCell>
                              {value}
                            </TableCell>
                          </TableRow>
                        );
                      })
                    }
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
                    {
                      state.info.pkg && Object.keys(state.info.pkg).map((key, i)=>{
                        let value = state.info.pkg[key];
                        return (
                          <TableRow key={i}>
                            <TableCell>
                              {key}
                            </TableCell>
                            <TableCell>
                              {value}
                            </TableCell>
                          </TableRow>
                        );
                      })
                    }
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