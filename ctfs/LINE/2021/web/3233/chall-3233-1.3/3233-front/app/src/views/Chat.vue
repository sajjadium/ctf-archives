<template>
  <div class="container">
    <div class="header">
      <div class="header-text">
        <h3>{{ to }}</h3>
      </div>
    </div>
    <div class="chat">
      <message
        v-for="message of ordered_messages"
        v-bind:key="message.id"
        v-bind:message="message"
      ></message>
    </div>
    <div class="form">
      <textarea v-model="body" />
      <button v-on:click="sendMessage" v-bind:disabled="disabled">Send</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { Manager } from 'socket.io-client'
import tweetnacl from 'tweetnacl'
import message from '../components/Message'
import crypto from 'browserify-aes'

export default {
  data: function () {
    return {
      from: this.$store.state.username,
      to: this.$route.params.username,
      body: '',
      socket: null,
      messages: {},
      ordered_messages: [],
      publicKeys: {},
      sharedSecrets: {}
    }
  },
  components: {
    message
  },
  methods: {
    getPublicKey: async function (username) {
      let publicKey
      if (this.publicKeys[username]) {
        publicKey = this.publicKeys[username]
      } else {
        const res = await axios.get(
          '/api/publicKey?username=' + encodeURIComponent(username)
        )
        publicKey = Uint8Array.from(res.data.split(','))
        this.publicKeys[username] = publicKey
      }
      return publicKey
    },
    calcSharedSecret: async function (username) {
      if (this.sharedSecrets[username]) return this.sharedSecrets[username]
      const publicKey = await this.getPublicKey(this.to)
      const secretKey = this.$store.state.secretKey
      const sharedSecret = tweetnacl.box.before(publicKey, secretKey)
      this.sharedSecrets[username] = sharedSecret
      return sharedSecret
    },
    sendMessage: async function () {
      // calc a shared secret
      const sharedSecret = await this.calcSharedSecret(this.to)

      // encrypt a message with shared secret
      const algorithm = 'aes-256-cbc'
      const iv = tweetnacl.randomBytes(16)
      const cipher = crypto.createCipheriv(algorithm, sharedSecret, iv)
      let encryptedData = cipher.update(this.body)
      encryptedData = Buffer.concat([encryptedData, cipher.final()])
      encryptedData = Buffer.from([...iv, ...encryptedData])

      // send an encrypted message
      this.socket.emit('message', {
        from: this.username,
        to: this.to,
        message: encryptedData
      })

      // clear body
      this.body = ''
    },
    onMessage: async function (data) {
      const isUserToMe = data.to === this.from
      const isMeToUser = data.from === this.from
      if (isUserToMe || isMeToUser) {
        const publicKeyUsername = isMeToUser ? data.to : data.from

        // calc a shared secret
        const sharedSecret = await this.calcSharedSecret(publicKeyUsername)

        // decrypt a message with shared secret
        const algorithm = 'aes-256-cbc'
        let encryptedData = new Uint8Array(data.message)
        const iv = encryptedData.subarray(0, 16)
        encryptedData = encryptedData.subarray(16)
        const decipher = crypto.createDecipheriv(algorithm, sharedSecret, iv)
        let encodedText = decipher.update(Buffer.from(encryptedData))
        encodedText = Buffer.concat([encodedText, decipher.final()])
        const text = new TextDecoder().decode(encodedText)

        // update message
        const message = {
          id: data.id,
          username: data.from,
          text: text,
          date: new Date(),
          is_read: false
        }
        this.ordered_messages.push(message)
        this.$set(this.messages, data.id, message)

        // send read event
        if (isUserToMe) {
          setTimeout(() => {
            this.socket.emit('read', { id: data.id })
          }, 200)
        }
      }
    },
    onRead: function (data) {
      if (this.messages[data.id]) {
        this.$set(this.messages[data.id], 'is_read', true)
      }
    }
  },
  mounted: function () {
    const manager = new Manager({
      path: '/api/socket'
    })
    this.socket = manager.socket('/')
    this.socket.emit('join', {
      room: [this.from, this.to].sort().join(':')
    })
    this.socket.on('message', this.onMessage)
    this.socket.on('read', this.onRead)
  },
  computed: {
    disabled: function () {
      return this.body.length === 0
    }
  },
  beforeDestroy: function () {
    this.socket.close()
  }
}
</script>

<style scoped>
.container {
  margin-left: auto;
  margin-right: auto;
  max-height: 100%;
  height: 100%;
  position: relative;
}

.header {
  display: flex;
  height: 10%;
  background-color: rgb(16, 29, 37);
  color: white;
  align-items: center;
  justify-content: center;
}

input {
  vertical-align: middle;
}

.chat {
  background-color: #89c7de;
  height: 85%;
  overflow-y: scroll;
}

.form {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 5%;
  background-color: #595f61;
  color: #fff;
}

.wrap {
  display: block;
}

textarea {
  height: 60%;
  width: 80%;
  border-radius: 10px;
  margin-left: auto;
}

button {
  margin: 0 auto;
}
</style>
