import React from 'react';
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

import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

import DateFnsUtils from '@date-io/date-fns';
import { DateTimePicker, MuiPickersUtilsProvider } from "material-ui-pickers";

import List from '@material-ui/icons/List';
import Save from '@material-ui/icons/Save';
import Delete from '@material-ui/icons/Delete';

import DeleteConfirmDialog from '../Dialogs/DeleteConfirmDialog';
import Util from '../../common/util';

class MainEdit extends React.PureComponent{
  state = {
    schema: [],
    foreignKeys: [],
    showData: [],
    params: [],
    isOpenDelete: false,
  }

  getSchema=(model)=>{
    const self = this;
    Util.getAPI('/admin/api/schema/'+model)
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

  //============ Delete ============
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

    //const id = event.currentTarget.dataset.id;
    const id = this.props.store.state.targetId;
    const url = '/admin/api/'+model+'/'+id+'/delete';

    Util.deleteAPI(url)
    .then(response=>{
      this.props.history.push('../');
    })
    .catch(err=>{
      console.error(err);
    })
  }

  //============ Save ============
  setParam=(event)=>{
    let new_params = this.state.showData;
    const key = event.currentTarget.name;
    new_params[key] = event.currentTarget.value;
    this.setState({showData: new_params});
  }

  setPramDateTime=(key, value)=>{
    let new_params = this.state.showData;
    try{
      new_params[key] = value.toISOString();
    }catch(err){
      new_params[key] = value;
    }
    this.setState({showData: new_params});
    this.forceUpdate();
  }

  save=(event)=>{
    // get URL param
    const model = this.props.match.params.model;

    const id = event.currentTarget.dataset.id;
    const url = '/admin/api/'+model+'/'+id+'/patch';

    Util.postAPI(url, this.state.showData)
    .then(response=>{
      this.props.history.push('../'+id);
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

  render(){
    const { classes } = this.props;
    // get URL param
    const model = this.props.match.params.model;

    let html_row = [];
    const keys = Object.keys(this.state.foreignKeys);
    let i = 0;
    for(let key in this.state.showData){
      let show = this.state.showData[key]? this.state.showData[key]: '';

      if(key === 'id'){
        //IDの時
        html_row.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              <TextField
                defaultValue={show}
                name={key}
                multiline
                className={classes.textarea + ' params'}
                InputProps={{
                  readOnly: true,
                }}
              />
            </TableCell>
          </TableRow>
        );
      }else if(keys.includes(key)){
        //外部キーの問
        const options = []
        let selectedId;
        for(let i in this.state.foreignKeys[key]){
          const foreignData = this.state.foreignKeys[key][i];

          if(foreignData.id === show){
            selectedId = foreignData.id;
          }
          options.push(
            <option key={i} value={foreignData.id}>{foreignData.data}</option>
          );
        }

        html_row.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              <FormControl fullWidth className={classes.formControl}>
                <Select
                  defaultValue={selectedId}
                  onChange={this.setParam}
                  name={key}
                  className='params'
                  autoWidth
                  native
                >
                  {options}
                </Select>
              </FormControl>
            </TableCell>
          </TableRow>
        )
      }else if(this.state.schema[i][2] === 'DATETIME'){
        //datetime型の時
        html_row.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
              <TableCell>
                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                  <DateTimePicker
                    autoOk
                    ampm={false}
                    format="yyyy-MM-dd HH:mm:ss"
                    value={show}
                    onChange={this.setPramDateTime.bind(this, key)}
                    name={key}
                    label="24h clock"
                  />
                </MuiPickersUtilsProvider>
              </TableCell>
          </TableRow>
        );
      }else{
        //文字列の時
        html_row.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              <TextField
                defaultValue={show}
                onChange={this.setParam}
                name={key}
                multiline
                className={classes.textarea + ' params'}
              />
            </TableCell>
          </TableRow>
        );
      }
      i++;
    }

    return(
      <div>
        <h1>{model}</h1>
        <Card>
          <CardContent>
            <div className={classes.flex}>
              <p>Edit</p>
              <div className={classes.buttons}>
                <NavLink to='../'>
                  <Button variant="contained" className={classes.listButton}>
                    <List/>list
                  </Button>
                </NavLink>
                <Button variant="contained" className={classes.saveButton} data-id={this.props.match.params.id} onClick={this.save}>
                  <Save/>save
                </Button>
                <Button variant="contained"
                  onClick={this.openDelete}
                  data-id={this.props.match.params.id}
                  className={classes.deleteButton}
                >
                  <Delete/>delete
                </Button>
              </div>
            </div>
            <Divider />
            <div className={classes.scroll}>
              <Table>
                <TableBody>
                  {html_row}
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
  saveButton: {
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

export default withStyles(styles)(withRouter(withStore(MainEdit)));