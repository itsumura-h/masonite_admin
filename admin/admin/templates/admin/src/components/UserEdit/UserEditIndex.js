import React, {PureComponent} from 'react';
import { withStyles } from '@material-ui/core/styles';

import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';

import Util from '../../common/util';

class UserEditIndex extends PureComponent{

  getUsers=()=>{

  }

  render(){
    return(
      <div>
        <Card>
            <CardContent>
              <p>aaa</p>
            </CardContent>
        </Card>
      </div>
    );
  }
}

const styles = {
}

export default withStyles(styles)(UserEditIndex);