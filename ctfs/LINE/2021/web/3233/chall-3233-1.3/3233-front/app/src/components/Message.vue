<template>
  <div class="message" v-bind:class="{ right: isRight, left: !isRight }">
    <div class="wrap">
      <div class="username">{{ message.username }}</div>
      <div class="message-box">
        <div class="meta" v-if="isRight"><div v-if="message.is_read">read</div><div>{{ format }}</div></div>
        <div class="text">{{ message.text }}</div>
        <div class="meta" v-if="!isRight"><div v-if="message.is_read">read</div><div>{{ format }}</div></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    message: Object,
    isRead: Boolean
  },
  computed: {
    format: function () {
      return `${this.message.date.getHours()}:${this.message.date.getMinutes()}`
    },
    isRight: function () {
      return this.message.username === this.$store.state.username
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.message {
  width: 100%;
  text-align: right;
}

.message.left {
  text-align: left;
}

.message.right {
  text-align: right;
}

.wrap {
  margin: 10px;
}

.username {
  font-size: 12px;
  padding-left: 5px;
  padding-bottom: 5px;
}

.left.message-box {
  text-align: left;
}

.right.message-box {
  text-align: right;
}

.text {
  max-width: 250px;
  border-radius: 6px;
  display: inline-block;
  padding: 5px;
  padding-left: 10px;
  padding-right: 10px;
  text-align: left;
  overflow-wrap: break-word;
  word-break: break-all;
}

.left .text {
  background-color: white;
}

.right .text {
  background-color: lawngreen;
}

.meta {
  display: inline-block;
  font-size: 12px;
  margin: 0 5px;
  vertical-align: bottom;
}
</style>
