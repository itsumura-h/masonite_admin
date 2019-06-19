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

class MainIndex extends PureComponent {
  state = {
    indexData: [],
    isOpenDelete: false,
    page: 0,
    count: 0,
  }

  //========================== API Access ==========================
  getIndex=(model, page=this.state.page)=>{
    const self = this;
    const params = {p: page+1, i: this.props.store.get('rowsPerPage')};
    Util.getAPI('/admin/api/'+model, params)
    .then(response=>{
      self.setState({
        indexData: response.data,
      });
    });
  }

  getPages=(model)=>{
    const self = this;
    Util.getAPI('/admin/api/'+model+'/count')
    .then(response=>{
      self.setState({count: Number(response.data.count)});
    })
  }

  //========================== Delete ==========================
  openDelete=(event)=>{
    if(event){
      this.props.store.set('targetId')(event.currentTarget.dataset.id);
    }

    const newIsOpenDelete = this.state.isOpenDelete? false: true;
    this.setState({isOpenDelete: newIsOpenDelete});
  }

  delete=(event)=>{
    // get URL param
    const model = this.props.match.params.model;

    const id = this.props.store.get('targetId');
    const url = '/admin/api/'+model+'/'+id+'/delete';

    Util.deleteAPI(url)
    .then(response=>{
      this.setState({page: 0});
      this.getPages(model);
      this.getIndex(model, 0);
    })
    .catch(err=>{
      console.error(err);
    })
  }

  //========================== Pagenation ==========================
  handleChangePage=(event, page)=>{
    this.setState({page: Number(page)});
    const model = this.props.match.params.model;
    this.getIndex(model, page);
    window.scrollTo(0,0); // scroll to the top
  };

  handleChangeRowsPerPage=(event)=>{
    this.setState({page: 0});
    this.props.store.set('rowsPerPage')(Number(event.target.value));
  };


  //========================== React ==========================
  componentDidMount(){
    // get URL param
    const model = this.props.match.params.model;

    if(model){
      this.getIndex(model);
      this.getPages(model);
      Util.setModelTitle();
    }
  }

  componentDidUpdate(nextProps){
    // get URL param
    const model = this.props.match.params.model;

    if(this.props.match.params.model !== nextProps.match.params.model ||
      this.props.store.get('rowsPerPage') !== nextProps.store.get('rowsPerPage')){
      this.setState({page: 0});
      this.getIndex(model, 0);
      this.getPages(model);
    }

    if(this.props !== nextProps){
      Util.setModelTitle();
    }
  }

  render() {
    const { classes, store } = this.props;
    // get URL param
    const model = this.props.match.params.model;
    // pagenation
    // set range of array
    const rowsPerPage = store.get('rowsPerPage');

    let headers = [];
    let html_table = [];
    if(this.state.indexData && this.state.indexData[0]){
      const td_key = Object.keys(this.state.indexData[0]).length;
      headers = Object.keys(this.state.indexData[0]);
      headers.push('show', 'edit', 'delete');

      this.state.indexData.forEach((row, i)=>{
        let row_html = [
          Object.keys(row).map((key)=>{
            return <TableCell key={key}>{row[key]}</TableCell>
          })
        ];

        row_html.push( // Button
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
      });
    }

    return (
      <div>
        <h1>{store.get('modelStr')['str']}</h1>
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
                    {
                      headers.map((header, i)=>{
                        return <TableCell key={i}>{header}</TableCell>
                      })
                    }
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
