<template>
  <b-container id="app" dir="rtl">
    <router-view/>
  </b-container>
</template>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Lateef&display=swap');
html, body {
  font-family: 'Lateef', sans-serif !important;
  font-size: x-large;
}

#app {
  font-family: 'Lateef', sans-serif;

  //font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
#plus {
  padding: 0 20px 0 20px;
  display: inline-block;
  font-size: 50px;
  vertical-align: top;
  line-height: 100px;
}

</style>
