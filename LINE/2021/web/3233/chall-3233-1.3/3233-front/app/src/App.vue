<template>
  <div id="app">
    <div id="view">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style>
body {
  margin: 0;
}

h1,
h2,
h3 {
  margin: 0;
  color: white;
}
h1 {
  font-size: 80px;
}

h2 {
  font-size: 60px;
}

h3 {
  font-size: 40px;
}

a {
  font-size: 20px;
  text-decoration: none;
  color: white;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

#view {
  width: 100%;
  height: 100%;
  max-height: 1000px;
  max-width: 500px;
}

.home {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: 100%;
  background-color: #74b98b;
  color: white;
  overflow-y: scroll;
}

.button {
  font-size: 30px;
  padding: 0 30px;
  text-decoration: none;
  color: white;
  border: 1px solid white;
  border-radius: 3px;
  background-color: transparent;
}

input {
  font-size: 20px;
}
</style>
