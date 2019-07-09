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

import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

import DateFnsUtils from '@date-io/date-fns';
import { DateTimePicker, DatePicker, TimePicker, MuiPickersUtilsProvider } from "material-ui-pickers";

import List from '@material-ui/icons/List';
import Save from '@material-ui/icons/Save';
import Delete from '@material-ui/icons/Delete';

import DeleteConfirmDialog from '../Dialogs/DeleteConfirmDialog';
import Util from '../../common/util';

class MainEdit extends PureComponent{
  state = {
    schema: [],
    showData: null,
    foreignKeys: [],
    inputDataData: [],
    params: [],
    isOpenDelete: false,
    error: '',
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
    const url = `/admin/api/${model}/${id}/delete`;

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
    let new_params = this.state.params;
    const key = event.currentTarget.name;
    new_params[key] = event.currentTarget.value;
    this.setState({params: new_params});
    this.forceUpdate();
  }

  setPramDate=(key, value)=>{
    let new_params = this.state.params;
    new_params[key] = Util.dateToString(value, 'YYYY-MM-DD');
    this.setState({params: new_params});
    this.forceUpdate();
  }

  setPramDateTime=(key, value)=>{
    let new_params = this.state.params;
    new_params[key] = value.toLocaleString();
    this.setState({params: new_params});
    this.forceUpdate();
  }

  save=(event)=>{
    // get URL param
    const model = this.props.match.params.model;
    const id = event.currentTarget.dataset.id;
    const url = `/admin/api/${model}/${id}/put`;

    // Util.postAPI(url, this.state.params)
    Util.putAPI(url, this.state.params)
    .then(response=>{
      if(!response.data.error){
        this.props.history.push(`../${id}`);
      }else{
        this.setState({error: response.data.error});
      }
    })
    .catch(err=>{
      // if(err){this.setState({error: err})}
      // console.error(err);
      ;
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
    const keys = Object.keys(this.state.foreignKeys);

    return(
      <div>
        <h1>{store.get('modelStr')['str']}</h1>
        <p className={classes.error}>{this.state.error}</p>
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
                <Button variant="contained"
                  className={classes.saveButton}
                  data-id={this.props.match.params.id}
                  onClick={this.save}
                  disabled={Object.keys(this.state.params).length === 0? true: false}
                >
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
                  {
                    this.state.showData &&
                    Object.keys(this.state.showData).map((key, i)=>{
                      let inputData = this.state.showData[key]? this.state.showData[key]: '';

                      if(key === 'id'){
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                            <TableCell>
                              <TextField
                                defaultValue={inputData}
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
                      }else if(key === 'created_at' || key === 'updated_at'){
                        ; // skip
                      }else if(keys.includes(key)){
                        // when in foreign key
                        let selectedId;
                        const options = this.state.foreignKeys[key].map((foreignData, i2)=>{
                          if(foreignData.id === inputData){
                            selectedId = foreignData.id;
                          }
                          return <option key={i2} value={foreignData.id}>{foreignData.data}</option>
                        })

                        return (
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
                        );
                      }else if(this.state.schema[i]['type'] === 'DATE'){
                        // Date
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                              <TableCell>
                                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                                  <DatePicker
                                    format="yyyy-MM-dd"
                                    onChange={this.setPramDate.bind(this, key)}
                                    name={key}
                                    label="Date"
                                    value={this.state.params[key]? this.state.params[key]: inputData}
                                  />
                                </MuiPickersUtilsProvider>
                              </TableCell>
                          </TableRow>
                        );
                      }else if(this.state.schema[i]['type'] === 'DATETIME'){
                        // Datetime
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                              <TableCell>
                                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                                  <DateTimePicker
                                    ampm={false}
                                    format="yyyy-MM-dd HH:mm:ss"
                                    value={this.state.params[key]? this.state.params[key]: inputData}
                                    onChange={this.setPramDateTime.bind(this, key)}
                                    name={key}
                                    label="24h clock"
                                  />
                                </MuiPickersUtilsProvider>
                              </TableCell>
                          </TableRow>
                        );
                      }else if(this.state.schema[i]['type'] === 'TIME'){
                        // Time
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                              <TableCell>
                                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                                  <TimePicker
                                    ampm={false}
                                    format="HH:mm:ss"
                                    onChange={this.setPramDateTime.bind(this, key)}
                                    name={key}
                                    label="24h clock"
                                    value={this.state.params[key]? this.state.params[key]: inputData}
                                  />
                                </MuiPickersUtilsProvider>
                              </TableCell>
                          </TableRow>
                        );
                      }else if(this.state.schema[i]['type'] === 'TIMESTAMP'){
                        // TIMESTAMP
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                              <TableCell>
                                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                                  <DateTimePicker
                                    ampm={false}
                                    format="yyyy-MM-dd HH:mm:ss"
                                    onChange={this.setPramDateTime.bind(this, key)}
                                    name={key}
                                    label="24h clock"
                                    value={this.state.params[key]? this.state.params[key]: inputData}
                                  />
                                </MuiPickersUtilsProvider>
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
                                defaultValue={this.state.params[key]? this.state.params[key]: inputData}
                                onChange={this.setParam}
                                name={key}
                                multiline
                                className={classes.textarea + ' params'}
                              />
                            </TableCell>
                          </TableRow>
                        );
                      }
                      return false;
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
  error: {
    backgroundColor: 'yellow'
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