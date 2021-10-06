<template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
<<<<<<< HEAD
    <router-link to="/assigntrainers">Assign Trainers</router-link>
  </div>
  <router-view/>
</template>

<style>
=======
    <router-link to="/login">Login</router-link>
  </div>
  <router-view />
</template>

<style lang="scss">
>>>>>>> main
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
