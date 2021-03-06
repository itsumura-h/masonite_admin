import React, {PureComponent} from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import { withRouter } from 'react-router';
import {NavLink} from 'react-router-dom';

import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import TextField from '@material-ui/core/TextField';

import List from '@material-ui/icons/List';
import Edit from '@material-ui/icons/Edit';
import Delete from '@material-ui/icons/Delete';

import DeleteConfirmDialog from '../Dialogs/DeleteConfirmDialog';
import Util from '../../common/util';

class MainShow extends PureComponent{
  state = {
    schema: [],
    foreignKeys: [],
    showData: [],
    isOpenDelete: false
  }

  getSchema=(model)=>{
    const self = this;
    Util.getAPI('/admin/api/schema/'+model+'/detail')
    .then(response=>{
      self.setState({
        schema: response.data.schema,
        foreignKeys: response.data.foreign_keys
      });
    });
  }

  getShow=(model, id)=>{
    const self = this;
    Util.getAPI('/admin/api/'+model+'/'+id)
    .then(response=>{
      self.setState({showData: response.data});
    });
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
    const url = `/admin/api/${model}/${id}/delete`;

    Util.deleteAPI(url)
    .then(response=>{
      this.props.history.push('./');
    })
    .catch(err=>{
      console.error(err);
    })
  }

  componentDidMount(){
    // get URL param
    const model = this.props.match.params.model;
    const id = this.props.match.params.id;

    if(model){
      this.getSchema(model);
      this.getShow(model, id);
    }
  }

  componentDidUpdate(){
    Util.setModelTitle();
  }

  render(){
    const { classes, store } = this.props;
    // get URL param
    const id = this.props.match.params.id;
    const keys = Object.keys(this.state.foreignKeys);
    const permission = localStorage.getItem('permission');

    let buttons = null;
    if(permission < 3){
      buttons = (
        <div className={classes.buttons}>
          <NavLink to='./'>
            <Button variant="contained" className={classes.listButton}>
              <List/>list
            </Button>
          </NavLink>
          <NavLink to={`./${id}/edit`}>
            <Button variant="contained" className={classes.editButton}>
              <Edit/>edit
            </Button>
          </NavLink>
          <Button
            onClick={this.openDelete}
            data-id={this.props.match.params.id}
            variant="contained"
            className={classes.deleteButton}
          >
            <Delete/>delete
          </Button>
        </div>
      );
    }else{
      buttons = (
        <div className={classes.buttons}>
          <NavLink to='./'>
            <Button variant="contained" className={classes.listButton}>
              <List/>list
            </Button>
          </NavLink>
        </div>
      );
    }

    return(
      <div>
        <h1>{store.get('modelStr')['str']}</h1>
        <Card>
          <CardContent>
            <div className={classes.flex}>
              <p>Detail</p>
              {buttons}
            </div>
            <Divider />
            <div className={classes.scroll}>
              <Table>
                <TableBody>
                  {
                    Object.keys(this.state.showData).map((key, i)=>{
                      let show = this.state.showData[key]? this.state.showData[key]: '';

                      // when column is forwign key
                      if(keys.includes(key)){
                        let foreignValue, foreignId;
                        this.state.foreignKeys[key].some((foreignData)=>{
                          if(foreignData.id === show){
                            foreignValue = foreignData.data;
                            foreignId = foreignData.id;
                            return true;
                          }
                          return false;
                        })
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                            <TableCell>
                              <TextField
                                value={foreignValue}
                                data-id={foreignId}
                                InputProps={{
                                  readOnly: true,
                                }}
                                multiline
                                className={classes.textarea}
                              />
                            </TableCell>
                          </TableRow>
                        );
                      }else if(this.state.schema[i] && this.state.schema[i]['type'] === 'DATETIME'){
                        //datetime
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                              <TableCell>
                                <TextField
                                  value={new Date(show).toString()}
                                  data-id={key}
                                  InputProps={{
                                    readOnly: true,
                                  }}
                                  multiline
                                  className={classes.textarea}
                                />
                              </TableCell>
                          </TableRow>
                        );
                      }else if(this.state.schema[i] && this.state.schema[i]['type'] === 'TIME'){
                        //time
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                              <TableCell>
                                <TextField
                                  value={new Date(show).toTimeString().split(' ')[0]}
                                  data-id={key}
                                  InputProps={{
                                    readOnly: true,
                                  }}
                                  multiline
                                  className={classes.textarea}
                                />
                              </TableCell>
                          </TableRow>
                        );
                      }else{
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                            <TableCell>
                              <TextField
                                value={show}
                                InputProps={{
                                  readOnly: true,
                                }}
                                multiline
                                className={classes.textarea}
                              />
                            </TableCell>
                          </TableRow>
                        );
                      }
                    })
                  }
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
  textarea: {
    width: '90%'
  },
  flex: {
    display: 'flex'
  },
  buttons: {
    margin: '0 0 0 auto'
  },
  listButton: {
    color: 'black',
    backgroundColor: '#ECF0F5'
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

export default withStyles(styles)(withRouter(withStore(MainShow)));