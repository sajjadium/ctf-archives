const intervalID = window.setInterval(updateScreen, 200);
const console = document.getElementById("console");

const txt = [
  "FORCE: XX0022. ENCYPT://000.222.2345",
  "TRYPASS: ********* AUTH CODE: ALPHA GAMMA: 1___ PRIORITY 1",
  "RETRY: REINDEER FLOTILLA",
  "CONNECTED: EVILCORP HQ",
  "LOADING: OPERATION PIGEON",
  "REFRESH: HTTP://EVILCORP.COM/NOTES",
  "Z:> /SEEIA/GAMES/TICTACTOE/ EXECUTE -PLAYERS 0",
]

const docfrag = document.createDocumentFragment();

function updateScreen() {

  txt.push(txt.shift());

  txt.forEach(function(e) {
    const p = document.createElement("p");
    p.textContent = e;
    docfrag.appendChild(p);
  });

  while (console.firstChild) {
    console.removeChild(console.firstChild);
  }
  console.appendChild(docfrag);
}