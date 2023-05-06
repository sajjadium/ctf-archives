import {
  INPUT_EVENT_TYPE,
  COLOR,
  Chessboard,
  MARKER_TYPE,
} from "../cm-chessboard/Chessboard.js";

var game_over = false;

// get elements
const fen = document.getElementById("fen");
const setFEN = document.getElementById("setFEN");
const copyFEN = document.getElementById("copyFEN");
const reset = document.getElementById("reset");
const takeback = document.getElementById("takeback");
const makeMove = document.getElementById("makeMove");
const flipBoard = document.getElementById("flipBoard");
const aiMove = document.getElementById("aiMove");
const uiState = document.getElementById("uiState");
const thinkingTime = document.getElementById("thinkingTime");

// initialise engine
var game = new engine();

// initialise chessboard
const board = new Chessboard(document.getElementById("board"), {
  position: game.getFEN(),
  sprite: { url: "../assets/images/chessboard-sprite-staunty.svg" },
  animationDuration: 200,
});

updateStatus();

board.enableMoveInput(inputHandler);

// IO functions

function inputHandler(event) {
  event.chessboard.removeMarkers(MARKER_TYPE.dot);
  if (event.type === INPUT_EVENT_TYPE.moveInputStarted) {
    const moves = game.getMovesAtSquare(event.square);
    for (const move of moves) {
      // draw dots on possible squares
      event.chessboard.addMarker(MARKER_TYPE.dot, move);
    }
    return moves.length > 0;
  } else if (event.type === INPUT_EVENT_TYPE.validateMoveInput) {
    const result = game.move(event.squareFrom, event.squareTo);
    if (result) {
      event.chessboard.disableMoveInput();
      this.chessboard.state.moveInputProcess.then(() => {
        // wait for the move input process has finished
        this.chessboard.setPosition(game.getFEN(), true).then(() => {
          event.chessboard.enableMoveInput(inputHandler);
          setTimeout(() => {
            game.makeAIMove();
            this.chessboard.setPosition(game.getFEN(), true);
            setTimeout(() => updateStatus(), 300);
          }, 500);
        });
      });
    } else {
      console.warn("invalid move");
    }
    return result;
  }
}

// Check board status
function updateStatus() {
  if (game_over) return;

  // update FEN
  fen.value = game.getFEN();

  const status = game.gameStatus();

  if (status.over) {
    game_over = true;
    board.disableMoveInput();
    alert(status.over);
    uiState.innerHTML = `${status.over}!`;
    return false;
  } else {
    // update status
    status.check
      ? (uiState.innerHTML = "Check!")
      : (uiState.innerHTML =
          `${status.sideToMove[0].toUpperCase()}${status.sideToMove.slice(1)}` +
          " to move");
  }
}

// event listeners
reset.addEventListener("click", () => {
  if (window.confirm("Are you sure you want to reset the board?")) {
    game.reset();
    board.enableMoveInput(inputHandler);
    board.setPosition(game.getFEN(), true);
  }
});

takeBack.addEventListener("click", () => {
  alert("Just like life, in chess, there are no takebacks.");
});

makeMove.addEventListener("click", () => {
  setTimeout(() => {
    game.makeAIMove();
    board.setPosition(game.getFEN(), true);
    board.enableMoveInput(inputHandler);
  }, 500);
  updateStatus();
});

flipBoard.addEventListener("click", () => {
  board.setOrientation(board.getOrientation() === "w" ? "b" : "w", true);
});

copyFEN.addEventListener("click", () => {
  const fen = game.getFEN();
  navigator.clipboard
    .writeText(fen)
    .then(() => {
      alert("FEN copied to clipboard");
    })
    .catch(() => {
      alert("Oops, something went wrong.");
    });
});

setFEN.addEventListener("click", () => {
  const fenField = fen.value;
  game.setFEN(fenField);
  board.setPosition(fenField, true);
  updateStatus();
});

thinkingTime.addEventListener("change", () => {
  game.setThinkingTime(thinkingTime.value);
});
