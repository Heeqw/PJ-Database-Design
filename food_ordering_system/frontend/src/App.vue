<template>
  <div id="app">
    <AppHeader />
    <BreadCrumb />
    <router-view></router-view>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import BreadCrumb from '@/components/BreadCrumb.vue';
export default {
  name: 'App',
  components: {
    AppHeader,
    BreadCrumb
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
