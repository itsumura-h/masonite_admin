import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';
import Details from '@material-ui/icons/Details';
import Edit from '@material-ui/icons/Edit';
import Delete from '@material-ui/icons/Delete';


import {Link} from 'react-router-dom';

import Util from '../../common/util';

class MainIndex extends React.PureComponent {
  state = {
    indexData: []
  }

  getIndex=(table)=>{
    const self = this;
    Util.getAPI('/admin/api/' + table)
    .then(response=>{
      self.setState({indexData: response.data});
    })
  }

  delete=(event)=>{
    // URLパラメーター取得
    const model = this.props.match.params.model;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    const id = event.currentTarget.dataset.id;
    const url = '/admin/api/'+table+'/'+id+'/delete';

    Util.deleteAPI(url)
    .then(response=>{
      this.getIndex(table);
    })
    .catch(err=>{
      console.error(err);
    })
  }

  componentDidMount(){
    // URLパラメーター取得
    const model = this.props.match.params.model;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    if(table){
      this.getIndex(table);
    }
  }

  componentDidUpdate(nextProps){
    // URLパラメーター取得
    const model = this.props.match.params.model;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    if(this.props !== nextProps && table){
      this.getIndex(table);
    }
  }

  render() {
    const { classes } = this.props;
    // URLパラメーター取得
    const model = this.props.match.params.model;

    let html_headers = [];
    let html_table = [];
    if(this.state.indexData && this.state.indexData[0]){
      const td_key = Object.keys(this.state.indexData[0]).length;
      let headers = Object.keys(this.state.indexData[0]);
      headers.push('show', 'edit', 'delete');

      for(let i in headers){
        const header = headers[i];
        html_headers.push(<TableCell key={i}>{header}</TableCell>);
      }

      for(let i in this.state.indexData){
        const row = this.state.indexData[i];
        let row_html = [];
        for(let key in row){
          row_html.push(<TableCell key={key}>{row[key]}</TableCell>);
        }

        row_html.push(
          <TableCell key={td_key+1}>
            <Link to={'/admin/'+model+'/'+row.id}>
              <Fab aria-label="show">
                <Details />
              </Fab>
            </Link>
          </TableCell>,
          <TableCell key={td_key+2}>
            <Link to={'/admin/'+model+'/'+row.id+'/edit'}>
              <Fab color="primary" aria-label="edit">
                <Edit />
              </Fab>
            </Link>
          </TableCell>,
          <TableCell key={td_key+3}>
            <Fab color="secondary" aria-label="edit" data-id={row.id} onClick={this.delete}>
                <Delete />
              </Fab>
          </TableCell>,
        );
        html_table.push(<TableRow key={i}>{row_html}</TableRow>);
      }
    }

    return (
      <div>
        <h1>{model}</h1>
        <p>index</p>
        <div className={classes.scroll}>
          <Table>
            <TableHead>
              <TableRow>
                {html_headers}
              </TableRow>
            </TableHead>
            <TableBody>
              {html_table}
            </TableBody>
          </Table>
        </div>
      </div>
    );
  }
}

const styles = {
  scroll: {
    overflow: 'auto'
  }
}

export default withStyles(styles)(withStore(MainIndex));
