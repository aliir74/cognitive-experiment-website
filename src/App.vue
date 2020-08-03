<template>
  <b-container id="app" dir="rtl">
    <router-view/>
  </b-container>
</template>

<style lang="css">
@import url('https://fonts.googleapis.com/css2?family=Lateef&display=swap');
html, body {
  font-family: 'Lateef', sans-serif !important;
  font-size: max(2.5vh, 2vw);
}

#app {
  font-family: 'Lateef', sans-serif;

  //font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
