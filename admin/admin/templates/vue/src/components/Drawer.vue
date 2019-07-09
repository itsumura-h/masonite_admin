<template>
  <v-navigation-drawer
    stateless
    id="drawer"
    :value="drawerOpen"
  >
    <v-toolbar flat>
      <v-list>
        <v-list-tile>
          <v-list-tile-title class="title">
            Table List
          </v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-toolbar>

    <v-divider></v-divider>

    <v-list dense class="pt-0">
      <v-list-tile
        v-for="model in models"
        :key="model['str']"
      >
        <router-link :to="'/admin/' + model['en']">
          <v-list-tile-content>
            <v-list-tile-title>{{model['str']}}</v-list-tile-title>
          </v-list-tile-content>
        </router-link>
      </v-list-tile>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import store from '../store.js'

export default {
  name: 'Drawer',
  computed: {
    drawerOpen: () => {
      return store.state.drawerOpen
    },
    models: () => {
      return store.state.info.models
    }
  },
  data () {
    return {
      modile: null,
      items: [{ title: 'a' }, { title: 'b' }, { title: 'c' }, { title: 'd' }, { title: 'e' }]
    }
  },
  methods: {
  }
}
</script>

<style scoped>
#drawer {
  min-height: 100vh;
  width: 300px !important;
}
</style>
