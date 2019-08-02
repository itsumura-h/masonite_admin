import React, {PureComponent} from 'react';
import { withStyles } from '@material-ui/core/styles';

import { withRouter } from 'react-router';
import { NavLink } from 'react-router-dom';

import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import TextField from '@material-ui/core/TextField';

import Edit from '@material-ui/icons/Edit';

import Util from '../../common/util';

class MypageShow extends PureComponent{
  state = {
    showData: {},
  }

  //========================== API Access ==========================
  getShow=()=>{
    const self = this;
    Util.getApi(`/admin/api/mypage`)
    .then(response=>{
      self.setState({showData: response.data});
    });
  }

  //========================== React ==========================
  componentDidMount(){
    this.getShow();
  }

  render(){
    const { classes } = this.props;
    return (
      <div>
        <h1>Mypage</h1>
        <Card>
          <CardContent>
            <div className={classes.flex}>
              <p>Detail</p>
              <div className={classes.buttons}>
                <NavLink to={`/admin/auth/mypage/edit`}>
                  <Button variant="contained" className={classes.editButton}>
                    <Edit/>edit
                  </Button>
                </NavLink>
              </div>
            </div>
            <Divider />
            <div className={classes.scroll}>
              <Table>
                <TableBody>
                  {
                    this.state.showData &&
                    Object.keys(this.state.showData).map((key, i)=>{
                      return(
                        <TableRow key={i}>
                          <TableCell>
                            {key}
                          </TableCell>
                          <TableCell>
                            <TextField
                              value={this.state.showData[key]}
                              InputProps={{
                                readOnly: true,
                              }}
                              multiline
                              className={classes.textarea}
                            />
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
}

export default withStyles(styles)(withRouter(MypageShow));
