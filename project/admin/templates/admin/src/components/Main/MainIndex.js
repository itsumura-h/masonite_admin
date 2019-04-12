import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

import Link from 'react-router-dom/Link';

import Util from '../../common/util';

class MainIndex extends React.Component {
  state = {
    index: []
  }

  getIndex=()=>{
    // URLパラメーター取得
    const model = this.props.match.params.model;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    const self = this;
    Util.getAPI('/admin/api/' + table)
    .then(response=>{
      self.setState({index: response.data});
    })
  }

  componentDidMount(){
    this.getIndex();
  }

  componentDidUpdate(nextProps){
    if(this.props !== nextProps){
      this.getIndex();
    }
  }

  render() {
    const { classes } = this.props;
    // URLパラメーター取得
    const model = this.props.match.params.model;
    // storeからtableを取得
    const tableName = this.props.store.state.models[model];

    let html_headers = [];
    let html_table = [];
    if(this.state.index && this.state.index[0]){
      const headers = Object.keys(this.state.index[0]);

      for(let i in headers){
        const header = headers[i];
        html_headers.push(<TableCell key={i}>{header}</TableCell>);
      }

      for(let i in this.state.index){
        const row = this.state.index[i];
        let row_html = [];
        for(let key in row){
          row_html.push(<TableCell key={key}><Link to={'/admin/'+tableName+'/'+row.id}>{row[key]}</Link></TableCell>);
        }
        html_table.push(<TableRow key={i}>{row_html}</TableRow>);
      }
    }

    return (
      <div>
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
