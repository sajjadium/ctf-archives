<template>
  <div class="user">
    <div class="header">
      <h2>Users</h2>
      <p><input type="text" v-model="search" placeholder="filter" /></p>
    </div>
    <div class="list">
      <div v-for="user of filteredUser" v-bind:key="user">
        <router-link
          :to="{
            path: '/chat/:username',
            name: 'Chat',
            params: { username: user },
          }"
        >
          {{ user }}</router-link
        >
      </div>
    </div>
    <div class="footer">
      <p>
        <router-link to="/logout">Logout from {{ $store.state.username }}</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data: function () {
    return {
      users: [],
      search: ''
    }
  },
  computed: {
    filteredUser: function () {
      return this.search
        ? this.users.filter((user) => user.includes(this.search))
        : this.users
    }
  },
  methods: {
    getUsers: function () {
      axios.get('/api/users').then((res) => {
        this.users = res.data
      })
    }
  },
  mounted: function () {
    this.getUsers()
  }
}
</script>

<style scoped>
.user {
  height: 100%;
  background-color: #74b98b;
  width: 100%;
  text-align: center;
}

.header {
  height: 15%;
}

.list {
  height: 80%;
  padding: 0 10%;
  text-align: left;
  overflow-x: hidden;
  overflow-y: scroll;
}

.footer {
  height: 5%;
  color: white;
}
</style>
