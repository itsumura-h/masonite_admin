getSchema=()=>{
    // URLパラメーター取得
    const model = this.props.match.params.model;
    // storeからtableを取得
    const table = this.props.store.state.models[model];

    const self = this;
    axios.get('http://localhost:8000/admin/api/schema/'+ table)
    .then(response=>{
      if(response.headers['content-type'] === 'application/json; charset=utf-8'){
        self.setState({schema: response.data});
      }
    })
  }