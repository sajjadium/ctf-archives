
<template>
  <div style="display: flex; padding: 20px">
    <div style="width: 35%; margin-right: 30px; display: flex; flex-direction: column">
      <div>
        <input v-on:keyup.enter="search"  v-model="searchText" placeholder="Search Messages" style="font-size: 20px; border-width: 0; padding: 4px; border: none; outline: none; width: 100%; background: transparent; height:70px; " class="noscrollbar"/>
      </div>


      <div v-for="({selected}, name) in senders" v-bind:key="name">
        <div style="cursor: pointer; display: flex; padding: 20px 15px; background: #ffdd59; box-shadow: #ffdd59 0px 8px 24px;; border-radius: 5px; margin-top: 30px"
             @click="select(name)" v-if="selected">
          <div style="text-align: left" >
            <div style="font-weight: 600">{{ name }}</div>
            <div style="font-size: 0.9em; color: #666">Encrypted</div>
          </div>
          <div style="margin-left: auto">
            <div style="font-weight: 100; color: #666">4PM</div>
          </div>

        </div>
        <div style="display: flex; padding: 20px 15px;box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px; margin-top: 30px; border-radius: 5px; cursor: pointer " v-if="!selected" @click="select(name)" >
          <div style="text-align: left">
            <div style="font-weight: 600">{{ name }}</div>
            <div style="font-size: 0.9em; color: #aaa">Encrypted</div>
          </div>
          <div style="margin-left: auto">
            <div style="font-weight: 100; color: #666">4PM</div>
          </div>
        </div>
      </div>
      <div  style="display: flex; flex-direction: column; padding: 20px 15px 10px 15px;box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;; border-radius: 5px; cursor: pointer;margin-top: 30px">

        <div style="font-weight: 600;">
          + Create New Encrypted Channel!

        </div>
        <div>
          <input v-on:keyup.enter="createChat"  v-model="newChatName" placeholder="Username" style="font-size: 18px; border-width: 0;  border: none; outline: none; width: 100%; background: transparent; padding: 10px 0; " class="noscrollbar">
        </div>
      </div>

      <div  style="display: flex; flex-direction: column; padding: 20px 15px 10px 15px;box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;; border-radius: 5px; cursor: pointer;margin-top: 30px">

        <div style="font-weight: 600;padding: 0 0 15px 0" @click="clearAll">
          Purge This Account (Logout)
        </div>
      </div>
    </div>
    <div style="border-style: solid; border-width: 3px; border-color: #ffa801; width: 65%; height: 60vh; min-height: 400px; position: relative; display: flex; flex-direction: column; box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;; border-radius: 10px;;">
      <div style="text-align: center;">
        <div style="font-weight: 600; margin-top: 10px;">{{ this.currentSelected }}</div>
        <div style="font-size: 0.9em; color: #aaa">Encrypted Channel Established</div>
      </div>

      <div style="height: 100%;overflow-y: scroll;padding: 10px; " class="noscrollbar">
        <div v-for="(m, idx) in messages" v-bind:key="idx">
          <div v-if="m.sender === currentSelected">
            <div style="text-align: left; background: #ddd; padding: 10px; width: max-content; border-radius: 5px">{{ m.message }}</div>
            <div style="font-size: 0.7em; text-align: left; color: #ccc; margin-top: 1px">4:55 PM</div>
          </div>
          <div v-if="m.sender === currentSelected + '@self'">
            <div style="margin-left: auto; background: #ffa801; padding: 10px; width: max-content; border-radius: 5px; color: white">{{ m.message }}</div>
            <div style="font-size: 0.7em; text-align: right; color: #ccc; margin-top: 1px">4:55 PM</div>
          </div>
        </div>


      </div>

      <div style="backdrop-filter: blur(10px); background: rgba(238,238,238,.8); height: 90px; position: absolute; bottom: 0; width: 100%; display: flex; border-radius: 0 0 10px 10px">
        <textarea placeholder="Add your message" style="padding: 10px; border: none; outline: none; width: 100%; background: transparent; height:70px" class="noscrollbar" v-model="messageInput"></textarea>
        <div style="font-size: 0.9em; background: #ffa801; color: #fff; border-style: none; border-radius: 8px; padding: 5px; height: 20px; bottom: 0; right: 0; position: absolute; margin: 4px;cursor:pointer;" @click="sendMessage" >Encrypt & Send</div>
      </div>
    </div>

  </div>
</template>

<script>
/* eslint-disable */
export default {
  name: 'Messages',
  props: {
    msg: String
  },
  data(){
    return {
      messages: [],
      senders: {},
      hasInit: false,
      currentSelected: "",
      newChatName: "",
      messageInput: "",
      searchText: ""
    }
  },
  mounted(){
    console.log("started")
    this.fetchMessages()
    setInterval(this.fetchMessages, 3000)
  },
  methods: {
    fetchMessages(){
      let username = window.localStorage.getItem("username") || "anonymous";
      fetch(`/all_messages/${username}`).then(data => data.json()).then(json => {
        console.log(json)
        if (!json.success){
          // window.location.href = "/register"
          this.clearAll()
          return
        }
        this.messages = json.messages;
        let newSenders = {};
        json.messages.forEach(v => {
          const senderName = v.sender.endsWith("@self") ? v.sender.split("@")[0] : v.sender;
          if (!this.hasInit) {
            this.currentSelected = senderName;
            newSenders[senderName] = {selected: true}
            this.hasInit = true;
          }
          if (newSenders[senderName] === undefined)
            newSenders[senderName] = this.senders[senderName] || {selected: false}
        })
        if (newSenders[this.currentSelected] === undefined){
          newSenders[this.currentSelected] = {selected: true}
        }
        this.senders = newSenders;

      })
    },
    select(name) {
      this.senders[this.currentSelected].selected = false;
      this.currentSelected = name;
      this.senders[name].selected = true;
    },
    createChat(){
      this.senders[this.currentSelected].selected = false;
      this.senders[this.newChatName] = {selected: true};
      this.currentSelected = this.newChatName;
      this.newChatName = "";
    },
    sendMessage(){
      fetch("/send_messages/" + this.currentSelected, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        body: JSON.stringify({message: this.messageInput}),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
      }).then(resp => {
        this.fetchMessages();
      });
    },
    search(){
      window.location.href = '/search#' + this.searchText
    },
    clearAll(){
      fetch("/clear_all").then(r => {
        window.localStorage.setItem("username", "");
        window.location.href = "/register"
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.noscrollbar{
  scrollbar-width: none;  /* Firefox */
}
.noscrollbar::-webkit-scrollbar {
  display: none;
}

button {
  background: #3c40c6;
  color: #fff;
  border-style: none;
  border-radius: 4px;
}
</style>
