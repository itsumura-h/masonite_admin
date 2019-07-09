<template>
  <div id="app">
    <Toolbar/>
    <div class="rightContents">
      <Drawer/>
      <router-view :style="'margin-left: -'+drawerWidth+'px'" class="main" />
    </div>
  </div>
</template>

<script>
import Toolbar from '../Toolbar'
import Drawer from '../Drawer'
import store from '../../store'

export default {
  name: 'Auth',
  components: {
    Toolbar,
    Drawer
  },
  computed: {
    drawerWidth () {
      return store.state.drawerWidth
    }
  },
  mounted () {
    this.getInfo()
  },
  methods: {
    getInfo () {
      store.commit('getInfo')
    }
  }
}
</script>

<style scoped>
#app {
  min-height: 80vh;
}
.rightContents {
  display: flex;
}
.main {
  width: 100%;
  padding: 20px 30px 30px;
  background-color: #ECF0F5;
  min-height: 80vh;
}
</style>
