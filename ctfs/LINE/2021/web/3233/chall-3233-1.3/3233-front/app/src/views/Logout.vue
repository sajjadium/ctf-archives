<template>
  <div>
      <h1>Logout</h1>
  </div>
</template>

<script>
export default {
  methods: {
    logout: function () {
      this.$store.dispatch('logout')
      this.$router.push('/')
    }
  },
  created: function () {
    this.logout()
  }
}
</script>
