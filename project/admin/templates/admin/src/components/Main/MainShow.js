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
import Delete from '@material-ui/icons/Delete';

import Util from '../../common/util';

class MainShow extends React.PureComponent{
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

  delete=(event)=>{
    // get URL param
    const model = this.props.match.params.model;

    const id = event.currentTarget.dataset.id;
    const url = '/admin/api/'+model+'/'+id+'/delete';

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

      // when column is forwign key
      if(keys.includes(key)){
        let foreignValue, foreignId;
        for(let i in this.state.foreignKeys[key]){
          const foreignData = this.state.foreignKeys[key][i];
          if(foreignData.id == show){
            foreignValue = foreignData.name;
            foreignId = foreignData.id;
            break;
          }
        }
        html_row.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              <textarea type='text' value={foreignValue} data-id={foreignId} className={classes.textarea} readOnly ></textarea>
            </TableCell>
          </TableRow>
        );
        i++;
      }else{
        html_row.push(
          <TableRow key={key}>
            <TableCell>
              {key}
            </TableCell>
            <TableCell>
              <textarea type='text' value={show} className={classes.textarea} readOnly ></textarea>
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
            <p>Detail</p>
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
              <Button variant="contained" className={classes.deleteButton} data-id={this.props.match.params.id} onClick={this.delete}>
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