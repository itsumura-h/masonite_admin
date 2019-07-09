<template>
  <v-toolbar prominent>
    <v-toolbar-side-icon @click="drawerOpen"></v-toolbar-side-icon>
    <v-toolbar-title>
      <router-link to="/admin">Masonite Admin</router-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <div class="v-btn v-btn--flat theme--light">Welcome! user1</div>
      <v-btn flat>Logout</v-btn>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>
import store from '../store.js'

export default {
  name: 'Toolbar',
  methods: {
    drawerOpen () {
      store.commit('drawerOpen')
    }
  }
}
</script>

<style scoped>
p {
  height: 100%;
}
</style>
