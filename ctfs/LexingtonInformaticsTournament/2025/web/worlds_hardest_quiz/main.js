const ws = new WebSocket("ws://" + location.host + "/ws")

const input = document.getElementById("submission");

ws.onmessage = (event) => {
  let data = JSON.parse(event.data);
  document.getElementById("question").innerHTML = data["question"];
  input.value = ""
};

function start() {
  document.getElementById("pre").hidden = true;
  document.getElementById("main").hidden = false;
  submit("");
}

function submit() {
  ws.send(input.value);
}