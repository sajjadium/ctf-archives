const socket = io();

const urlInput = document.querySelector("#url-input");
const submitButton = document.querySelector("#submit");
const statusPow = document.querySelector("#status-pow");
const statusQueued = document.querySelector("#status-queued");
const queueCount = document.querySelector("#queue-count");
const statusProcessing = document.querySelector("#status-processing");
const processingVerb = document.querySelector("#processing-verb");
const timeRemaining = document.querySelector("#time-remaining");

let instanceStateChangeTime = 0;

setInterval(() => {
  let secondsRemaining = Math.floor(
    (instanceStateChangeTime - Date.now()) / 1000
  );
  timeRemaining.innerText =
    secondsRemaining > 2 ? `in ${secondsRemaining} seconds` : "imminently";
}, 250);

submitButton.addEventListener("click", async () => {
  let url = urlInput.value;
  urlInput.disabled = true;
  submitButton.disabled = true;
  socket.emit("submitJob", { url });
});

socket.on("challenge", (challenge) => {
  statusPow.style.display = "block";
  statusQueued.style.display = "none";
  statusProcessing.style.display = "none";
  let response = solveChallenge(challenge);
  socket.emit("submitChallenge", response);
});

socket.on("position", (position) => {
  statusPow.style.display = "none";
  statusQueued.style.display = "block";
  statusProcessing.style.display = "none";
  queueCount.innerText = position.toString();
});

socket.on("accepted", ({ response, launchingAt }) => {
  statusPow.style.display = "none";
  statusQueued.style.display = "none";
  statusProcessing.style.display = "block";
  processingVerb.innerText = "be launched";
  instanceStateChangeTime = launchingAt;
});

socket.on("processing", ({ response, until }) => {
  statusPow.style.display = "none";
  statusQueued.style.display = "none";
  statusProcessing.style.display = "block";
  processingVerb.innerText = "shut down";
  instanceStateChangeTime = until;
});

socket.on("done", () => {
  urlInput.disabled = false;
  submitButton.disabled = false;
  statusPow.style.display = "none";
  statusQueued.style.display = "none";
  statusProcessing.style.display = "none";
});

function solveChallenge(challenge) {
  let counter = 0;

  while (true) {
    if (counter % 1000 === 0) console.log(counter);
    let digest = sha256.update(challenge.prefix + counter).array();
    let value =
      (digest[0] << 24) |
      (digest[1] << 16) |
      (digest[2] << 8) |
      (digest[3] << 0);
    value >>>= 32 - challenge.difficulty;

    if (value === 0) {
      return counter.toString();
    }

    counter++;
  }
}
