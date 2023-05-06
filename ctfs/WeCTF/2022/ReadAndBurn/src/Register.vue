<template>
  <div style="display: flex; flex-direction: column; padding: 20px">

    <div style="border-style: solid; border-width: 3px; border-color: #ffa801; width: 30%; margin: 0 auto; height: max-content; position: relative; display: flex; flex-direction: column; box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;; border-radius: 10px;;">
      <h1 style="padding: 20px">Register</h1>

      <div>
        <input v-model="username" placeholder="Username" style="font-size: 20px; border-width: 0; padding: 20px; border: none; outline: none; width: 100%; background: transparent; height:70px; " class="noscrollbar">
      </div>

      <div style="background-color: #ffa801; padding: 10px; text-align: center; color: #fff; font-weight: 800; cursor: pointer" @click="register">Submit</div>
    </div>

  </div>
</template>

<script>
/* eslint-disable */

export default {
  name: "Register",
  data(){
    return {
      username: ""
    }
  },
  methods: {
    register(){
      fetch(`/api/register/${this.username}`).then(data => data.json()).then(json => {
        if (json.success){
          window.localStorage.setItem("username", this.username)
          window.location.href = "/"
        } else {
          alert(json.msg)
        }
      })
    }
  }
}
</script>

<style scoped>

</style>