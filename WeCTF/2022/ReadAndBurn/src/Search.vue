<template>
  <div style="display: flex; flex-direction: column; padding: 20px">

    <h3 style="">Searching - {{currentSearch}}</h3>
    <div  v-for="(m, idx) in this.results" v-bind:key="idx" style="border-style: solid; border-width: 3px; border-color: #ffa801; width: 100%; margin: 10px auto; height: max-content; position: relative; display: flex; flex-direction: column; box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;; border-radius: 10px;;">
      <div style="display: flex; padding: 20px 15px;box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;; border-radius: 5px; cursor: pointer">
        <div style="text-align: left">
          <div style="font-weight: 600">{{ m.sender }}</div>
          <div style="font-size: 0.9em; color: #aaa">{{ m.message }}</div>
        </div>
        <div style="margin-left: auto">
          <div style="font-weight: 100; color: #666">4PM</div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
/* eslint-disable */

export default {
  name: "Search",
  data(){
    return {
      results: [],
      currentSearch: ""
    }
  },
  mounted() {
    this.findMessages();
    window.onhashchange = this.findMessages
  },
  methods: {
    findMessages(){
      this.currentSearch = window.location.hash.slice(1);
      fetch("/search_all?find=" + this.currentSearch).then(r => r.json()).then(json => {
        if (json.success) {
          this.results = json.related_messages
        }
      })
    }
  }
}
</script>

<style scoped>

</style>