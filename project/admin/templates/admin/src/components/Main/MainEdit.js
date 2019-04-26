import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { withStore } from '../../common/store';

import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import { withRouter } from 'react-router';
import {NavLink} from 'react-router-dom';

import List from '@material-ui/icons/List';
import Edit from '@material-ui/icons/Edit';
import Save from '@material-ui/icons/Save';

import Util from '../../common/util';

class MainEdit extends React.PureComponent{
  state = {
    schema: [],
    foreignKeys: [],
    showData: [],
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

  save=(event)=>{
    // get URL param
    const model = this.props.match.params.model;

    const id = event.currentTarget.dataset.id;
    const url = '/admin/api/'+model+'/'+id+'/patch';

    Util.postAPI(url)
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
    const id = this.props.match.params.id;

    let i = 0;
    let html_row = [];
    const keys = Object.keys(this.state.foreignKeys);
    for(let key in this.state.showData){
      let show = this.state.showData[key]? this.state.showData[key]: '';

      if(keys.includes(key)){
        const options = []
        let selectedId;
        for(let i in this.state.foreignKeys[key]){
          const foreignData = this.state.foreignKeys[key][i];

          if(foreignData.id == show){
            selectedId = foreignData.id;
          }
          options.push(
            <option key={i} value={foreignData.id} >{foreignData.name}</option>
          );
        }

        html_row.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              <select defaultValue={selectedId}>
                {options}
              </select>
            </TableCell>
          </TableRow>
        )
        i++;
      }else{
        html_row.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              <textarea type='text' defaultValue={show} className={classes.textarea} ></textarea>
            </TableCell>
          </TableRow>
        );
        i++;
      }
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
}

export default withStyles(styles)(withRouter(withStore(MainEdit)));