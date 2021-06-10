<template>
  <div class="home">
    <div class="login">
      <p><input type="text" v-model="username" placeholder="username" /></p>
      <p><input type="password" v-model="password" placeholder="password" /></p>
      <p><button v-on:click="login" class="button">Signup / Login</button></p>
      <div class="error" v-if="error">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import tweetnacl from 'tweetnacl'

export default {
  data: function () {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    login: function () {
      const keyPair = tweetnacl.box.keyPair()
      axios
        .post('/api/login', {
          username: this.username,
          password: this.password,
          publicKey: keyPair.publicKey.toString()
        })
        .then(() => {
          this.$store.dispatch('login', {
            username: this.username,
            secretKey: keyPair.secretKey
          })
          this.$router.push('/users')
        }).catch(err => {
          this.error = err.response.data
        })
    }
  }
}
</script>

<style scoped>
.login {
  position: relative;
}

.error {
  position: absolute;
  width: 100%;
  bottom: -30px;
}
</style>
