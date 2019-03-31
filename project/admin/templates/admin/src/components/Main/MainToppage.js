import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import {Link, NavLink} from 'react-router-dom';

import Add from '@material-ui/icons/Add';
import Create from '@material-ui/icons/Create';

import axios from 'axios';

class MainToppage extends React.Component {
  state = {
    tables: []
  }

  tables=()=>{
    const self = this;
    axios.get('http://localhost:8000/admin/api/tables')
    .then(function(response){
      if(response.headers['content-type'] == 'application/json; charset=utf-8'){
        self.setState({tables: response.data});
      }
    })
  }

  componentDidMount(){
    this.tables();
  }
  render() {
    const { classes } = this.props;

    let tables = [];
    let i = 0;
    for(let table of this.state.tables){
      tables.push(
        <TableRow key={i}>
          <TableCell align="left">
            <NavLink to={"admin/"+table} className={classes.link}>{table}</NavLink>
          </TableCell>
          <TableCell align="right">
            <NavLink to={"admin/"+table+"/create"} className={classes.link}><Add/>追加</NavLink>
          </TableCell>
        </TableRow>
      );
      i++;
    }

    return (
      <div>
        <h1>サイト管理</h1>
          <Table className={classes.table}>
          <TableBody>
            {tables}
          </TableBody>
          </Table>
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
  }
}

export default withStyles(styles)(MainToppage);