import React, {PureComponent} from 'react';
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
import TablePagination from '@material-ui/core/TablePagination';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Fab from '@material-ui/core/Fab';

import Add from '@material-ui/icons/Add';
import Details from '@material-ui/icons/Details';
import Edit from '@material-ui/icons/Edit';
import Delete from '@material-ui/icons/Delete';

import Util from '../../common/util';
import DeleteConfirmDialog from '../Dialogs/DeleteConfirmDialog';

class ManageAdminUserIndex extends PureComponent{
  state = {
    indexData: [],
    isOpenDeleteConfirm: false,
    page: 0,
    count: 0,
  }

  //========================== API Access ==========================
  getIndex=(page=this.state.page)=>{
    const self = this;
    const params = {p: page+1, i: this.props.store.get('rowsPerPage')};
    Util.getAPI('/admin/api/manage_admin_users', params)
    .then(response=>{
      self.setState({
        count: response.data.count,
        indexData: response.data.admin_users,
      });
    });
  }

  //========================== Delete ==========================
  openDelete=(event)=>{
    if(event){
      this.props.store.set('targetId')(event.currentTarget.dataset.id);
    }

    const newIsOpenDelete = this.state.isOpenDeleteConfirm? false: true;
    this.setState({isOpenDeleteConfirm: newIsOpenDelete});
  }

  delete=(event)=>{
    // get URL param
    const id = this.props.store.get('targetId');
    const url = `/admin/api/manage_admin_users/${id}/delete`;

    Util.deleteAPI(url)
    .then(response=>{
      this.setState({page: 0});
      this.getIndex(0);
    })
    .catch(err=>{
      console.error(err);
    })
  }

  //========================== Pagenation ==========================
  handleChangePage=(event, page)=>{
    this.setState({page: Number(page)});
    this.getIndex(page);
    window.scrollTo(0,0); // scroll to the top
  };

  handleChangeRowsPerPage=(event)=>{
    this.setState({page: 0});
    this.props.store.set('rowsPerPage')(Number(event.target.value));
  };

  //========================== React ==========================
  componentDidMount(){
    this.getIndex();
  }

  componentDidUpdate(nextProps){
    if(this.props.store.get('rowsPerPage') !== nextProps.store.get('rowsPerPage')){
      this.setState({page: 0});
      this.getIndex(0);
    }
  }

  render(){
    const { classes, store } = this.props;
    const rowsPerPage = store.get('rowsPerPage');

    return(
      <div>
        <h1>Admin Users</h1>
        <Card>
          <CardContent>
            <div className={classes.flex}>
              <p>index</p>
              <div className={classes.buttons}>
                <NavLink to={'/admin/ManageAdminUser/create'}>
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
                    <TablePagination
                      rowsPerPageOptions={[10, 20, 30, 50, 100]}
                      colSpan={2}
                      count={this.state.count}
                      rowsPerPage={rowsPerPage}
                      page={this.state.page}
                      SelectProps={{
                        native: true,
                      }}
                      onChangePage={this.handleChangePage}
                      onChangeRowsPerPage={this.handleChangeRowsPerPage}
                    />
                  </TableRow>
                  <TableRow>
                    <TableCell key={0}>ID</TableCell>
                    <TableCell key={1}>name</TableCell>
                    <TableCell key={2}>email</TableCell>
                    <TableCell key={3}>permission</TableCell>
                    <TableCell key={4}>show</TableCell>
                    <TableCell key={5}>edit</TableCell>
                    <TableCell key={6}>delete</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {
                    this.state.indexData.length > 0 &&
                    this.state.indexData.map((row, i)=>{
                      const key = 0;
                      return(
                        <TableRow key={i}>
                          <TableCell key={key}>
                            {row.id}
                          </TableCell>
                          <TableCell key={key+1}>
                            {row.name}
                          </TableCell>
                          <TableCell key={key+2}>
                            {row.email}
                          </TableCell>
                          <TableCell key={key+3}>
                            {row.permission}
                          </TableCell>
                          <TableCell key={key+4}>
                            <Link to={`/admin/ManageAdminUser/${row.id}`}>
                              <Fab aria-label="show">
                                <Details />
                              </Fab>
                            </Link>
                          </TableCell>
                          <TableCell key={key+5}>
                            <Link to={`/admin/ManageAdminUser/${row.id}/edit`}>
                              <Fab aria-label="edit" className={classes.editButton}>
                                <Edit />
                              </Fab>
                            </Link>
                          </TableCell>
                          <TableCell key={key+6}>
                            <Fab
                              aria-label="delete"
                              data-id={row.id}
                              onClick={this.openDelete}
                              className={classes.deleteButton}
                            >
                              <Delete />
                              </Fab>
                          </TableCell>
                        </TableRow>
                      );
                    })
                  }
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
        <DeleteConfirmDialog
          isOpen={this.state.isOpenDeleteConfirm}
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

export default withStyles(styles)(withStore(ManageAdminUserIndex));
