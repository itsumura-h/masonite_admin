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

import List from '@material-ui/icons/List';
import Save from '@material-ui/icons/Save';

import DateFnsUtils from '@date-io/date-fns';
import { DateTimePicker, DatePicker, TimePicker, MuiPickersUtilsProvider } from "material-ui-pickers";

import Util from '../../common/util';


class ResourceCreate extends PureComponent {
  state = {
    schema: [],
    foreignKeys: [],
    params: [],
    error: ''
  }

  getSchema=(model)=>{
    const self = this;
    Util.getApi(`/admin/api/schema/create/${model}`)
    .then(response=>{
      const schema = response.data.schema;
      const foreignKeys = response.data.foreign_keys;
      self.setState({
        schema: schema,
        foreignKeys: foreignKeys
      });

      this.setDefaultParam(schema, foreignKeys);
    });
  }

  //============ Save ============
  setDefaultParam=(schema, foreignKeys)=>{
    const keys = Object.keys(foreignKeys);
    let new_params = {};

    schema.forEach((row, i)=>{
      if(keys.includes(row['column'])){
        new_params[row['column']] = foreignKeys[row['column']][0]? foreignKeys[row['column']][0].id: null;
      }else{
        new_params[row['column']] = null;
      }
    });
    this.setState({params: new_params});
  }

  setParam=(event)=>{
    let new_params = this.state.params;
    const key = event.currentTarget.name;
    new_params[key] = event.currentTarget.value;
    this.setState({params: new_params});
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
    const url = `/admin/api/${model}`;

    Util.postApi(url, this.state.params)
    .then(response=>{
      if(!response.data.error){
        this.props.history.push('./');
      }else{
        this.setState({error: response.data.error});
      }
    })
    .catch(err=>{
      console.error(err);
    })
  }

  componentDidMount(){
    // get URL param
    const model = this.props.match.params.model;

    if(model){
      this.getSchema(model);
    }
  }

  componentDidUpdate(){
    Util.setModelTitle();
  }

  render(){
    const { classes, store } = this.props;
    const keys = Object.keys(this.state.foreignKeys);

    return(
      <div>
        <h1>{store.get('modelStr')['str']}</h1>
        <p className={classes.error}>{this.state.error}</p>
        <Card>
          <CardContent>
            <div className={classes.flex}>
              <p>create</p>
              <div className={classes.buttons}>
                <NavLink to='./'>
                  <Button variant="contained" className={classes.listButton}>
                    <List/>list
                  </Button>
                </NavLink>
              </div>
            </div>
            <Divider />
            <div className={classes.scroll}>
              <Table>
                <TableBody>
                  {
                    this.state.schema.map((column, i)=>{
                      const key = column['column'];

                      if(key === 'id'){
                        ; //don't display
                      }else if(keys.includes(key)){
                        //Foreign Key
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                            <TableCell>
                              <FormControl fullWidth className={classes.formControl}>
                                <Select
                                  onChange={this.setParam}
                                  name={key}
                                  className='params'
                                  autoWidth
                                  native
                                >
                                  {
                                    this.state.foreignKeys[key].map((foreignData, i)=>{
                                      return  <option key={i} value={foreignData.id}>{foreignData.data}</option>
                                    })
                                  }
                                </Select>
                              </FormControl>
                            </TableCell>
                          </TableRow>
                        );
                      }else if(column['type'] === 'DATE'){
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
                                    value={this.state.params[key]? this.state.params[key]: null}
                                  />
                                </MuiPickersUtilsProvider>
                              </TableCell>
                          </TableRow>
                        );
                      }else if(column['type'] === 'DATETIME'){
                        // DateTime
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
                                    label="Date and 24h clock"
                                    value={this.state.params[key]? this.state.params[key]: null}
                                  />
                                </MuiPickersUtilsProvider>
                              </TableCell>
                          </TableRow>
                        );
                      }else if(column['type'] === 'TIME'){
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
                                    value={this.state.params[key]? this.state.params[key]: null}
                                  />
                                </MuiPickersUtilsProvider>
                              </TableCell>
                          </TableRow>
                        );
                      }else if(column['type'] === 'TIMESTAMP'){
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
                                    label="Date and 24h clock"
                                    value={this.state.params[key]? this.state.params[key]: null}
                                  />
                                </MuiPickersUtilsProvider>
                              </TableCell>
                          </TableRow>
                        );
                      }else if(column['type'] === 'INTEGER'){
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                            <TableCell>
                              <TextField
                                onChange={this.setParam}
                                name={key}
                                type="number"
                                className={classes.textarea + ' params'}
                                InputLabelProps={{
                                  shrink: true,
                                }}
                              />
                            </TableCell>
                          </TableRow>
                        );
                      }else{
                        //toString
                        return (
                          <TableRow key={key}>
                            <TableCell>
                              {key}
                            </TableCell>
                            <TableCell>
                              <TextField
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
            <Divider />
            <div className={classes.flex}>
              <Button variant="contained" className={classes.saveButton} data-id={this.props.match.params.id} onClick={this.save}>
                <Save/>save
              </Button>
            </div>
          </CardContent>
        </Card>
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
  resetButton: {
    color: 'white',
    backgroundColor: '#F39C12',
    '&:hover': {
      backgroundColor: '#E38C02',
    },
  },
  saveButton: {
    margin: '0 0 0 auto',
    color: 'white',
    backgroundColor: '#3C8DBC',
    '&:hover': {
      backgroundColor: '#2C7DAC',
    },
  },
}

export default withStyles(styles)(withRouter(withStore(ResourceCreate)));
