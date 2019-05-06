import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import {NavLink} from 'react-router-dom';
import {Link} from 'react-router-dom';

import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Fab from '@material-ui/core/Fab';

import Add from '@material-ui/icons/Add';
import Details from '@material-ui/icons/Details';
import Edit from '@material-ui/icons/Edit';
import Delete from '@material-ui/icons/Delete';

import Util from '../../common/util';
import DeleteConfirmDialog from '../Dialogs/DeleteConfirmDialog';

class MainIndex extends React.PureComponent {
  state = {
    indexData: [],
    isOpenDelete: false
  }

  getIndex=(model)=>{
    const self = this;
    Util.getAPI('/admin/api/' + model)
    .then(response=>{
      self.setState({indexData: response.data});
    })
  }

  openDelete=(event)=>{
    if(event){
      const store = this.props.store;
      store.set('targetId')(event.currentTarget.dataset.id);
    }

    const newIsOpenDelete = this.state.isOpenDelete? false: true;
    this.setState({isOpenDelete: newIsOpenDelete});
  }

  delete=(event)=>{
    // get URL param
    const model = this.props.match.params.model;

    const id = this.props.store.state.targetId;
    const url = '/admin/api/'+model+'/'+id+'/delete';

    Util.deleteAPI(url)
    .then(response=>{
      this.getIndex(model);
    })
    .catch(err=>{
      console.error(err);
    })
  }

  componentDidMount(){
    // get URL param
    const model = this.props.match.params.model;

    if(model){
      this.getIndex(model);
    }
  }

  componentDidUpdate(nextProps){
    // get URL param
    const model = this.props.match.params.model;

    if(this.props !== nextProps && model){
      this.getIndex(model);
    }
  }

  render() {
    const { classes } = this.props;
    // get URL param
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
              <Fab aria-label="edit" className={classes.editButton}>
                <Edit />
              </Fab>
            </Link>
          </TableCell>,
          <TableCell key={td_key+3}>
            <Fab
              aria-label="delete"
              data-id={row.id}
              onClick={this.openDelete}
              className={classes.deleteButton}
            >
              <Delete />
              </Fab>
          </TableCell>
        );
        html_table.push(<TableRow key={i}>{row_html}</TableRow>);
      }
    }

    return (
      <div>
        <h1>{model}</h1>
        <Card>
          <CardContent>
            <div className={classes.flex}>
              <p>index</p>
              <div className={classes.buttons}>
                <NavLink to={'/admin/'+model+'/create'}>
                  <Button variant="contained" className={classes.newButton}>
                    <Add/>New
                  </Button>
                </NavLink>
              </div>
            </div>
            <Divider />
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
          </CardContent>
        </Card>
        <DeleteConfirmDialog
          isOpen={this.state.isOpenDelete}
          openDelete={this.openDelete}
          handleOkMethod={this.delete}
        />
      </div>
    );
  }
}

const styles = {
  scroll: {
    overflow: 'auto'
  },
  flex: {
    display: 'flex'
  },
  buttons: {
    margin: '0 0 0 auto'
  },
  newButton: {
    color: 'white',
    backgroundColor: '#00A65A',
    '&:hover': {
      backgroundColor: '#00964A',
    },
  },
  editButton: {
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
  }
}

export default withStyles(styles)(withStore(MainIndex));
