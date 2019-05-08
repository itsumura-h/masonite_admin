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

import List from '@material-ui/icons/List';
import Save from '@material-ui/icons/Save';

import DateFnsUtils from '@date-io/date-fns';
import { DateTimePicker, MuiPickersUtilsProvider } from "material-ui-pickers";

import Util from '../../common/util';


class MainCreate extends React.Component {
  state = {
    schema: [],
    foreignKeys: [],
    params: [],
    createDisplay: [],
  }

  getSchema=(model)=>{
    const self = this;
    Util.getAPI('/admin/api/schema/'+model+'/create')
    .then(response=>{
      self.setState({
        schema: response.data.schema,
        foreignKeys: response.data.foreign_keys
      });
    });
  }

  getCreateDisplay=(model)=>{
    const self = this;
    Util.getAPI('/admin/api/create_display/'+model)
    .then(response=>{
      self.setState({createDisplay: response.data});

      // set default value in foreign key
      const keys = Object.keys(this.state.foreignKeys);
      let new_params = [];
      for(let i in response.data){
        const column = response.data[i];
        if(keys.includes(column)){
          new_params[column] = '1';
        }else{
          new_params[column] = '';
        }
      }
      this.setState({params: new_params});
    });
  }

  //============ Save ============
  setParam=(event)=>{
    let new_params = this.state.params;
    const key = event.currentTarget.name;
    new_params[key] = event.currentTarget.value;
    this.setState({params: new_params});
  }

  setPramDateTime=(key, value)=>{
    let new_params = this.state.params;
    try{
      new_params[key] = value.toISOString();
    }catch(err){
      new_params[key] = value;
    }
    this.setState({params: new_params});
    this.forceUpdate();
  }

  save=(event)=>{
    // get URL param
    const model = this.props.match.params.model;
    const url = '/admin/api/'+model;

    Util.postAPI(url, this.state.params)
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

    if(model){
      this.getSchema(model);
      this.getCreateDisplay(model);
    }
  }

  render(){
    const { classes } = this.props;
    const model = this.props.match.params.model;

    let html_row = [];
    const keys = Object.keys(this.state.foreignKeys);
    for(let i in this.state.schema){
      const column = this.state.schema[i];

      const key = column[1];
      if(this.state.createDisplay.length > 0 && !this.state.createDisplay.includes(key)){
        continue;
      }else{
        if(column[2] === 'DATETIME'){
          // DateTime
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
                      onChange={this.setPramDateTime.bind(this, key)}
                      name={key}
                      label="24h clock"
                    />
                  </MuiPickersUtilsProvider>
                </TableCell>
            </TableRow>
          );
        }else if(keys.includes(key)){
          //Foreign Key
          const options = []
          for(let i in this.state.foreignKeys[key]){
            const foreignData = this.state.foreignKeys[key][i];

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
        }else if(key === 'id'){
          continue;
        }else{
          //文字列の時
          html_row.push(
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
      }
    }

    return(
      <div>
        <h1>{model}</h1>
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
                  {html_row}
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

export default withStyles(styles)(withRouter(withStore(MainCreate)));