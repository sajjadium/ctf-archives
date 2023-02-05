// sorry for the spaghetti

const moveSnd = new Audio("/mp3/move.mp3");
const engine = $("#engine")[0].contentWindow;

const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
const id = [...crypto.getRandomValues(new Uint8Array(16))].map(v => alphabet[v % alphabet.length]).join("");

let state, board, hovering = [];
const send = (msg) => engine.postMessage({ ...msg, id }, location.origin);

const getSquare = (sq) => $('#chessboard .square-' + sq);
const isDark = (sq) => sq.hasClass('black-3c85d');

window.onmessage = (e) => {
    if (e.data === "ready") {
        send({ type: "init" });
        return;
    }

    if (e.data.id !== id) {
        return;
    }

    if (e.data.type === "init") {
        board = Chessboard('chessboard', {
            draggable: true,
            position: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            onDragStart: (source) => state.moves.some(s => s.startsWith(source)),
            onDrop: (source, target) => {
                let action = `${source}${target}`;
                 // force promotion to queen, sorry, we don't have enough budget for this
                if (!state.moves.includes(action) && !state.moves.includes(action + "q"))
                    return "snapback";
                if (!state.moves.includes(action)) // promotion
                    action += "Q";
                moveSnd.play();
                send({ type: "play_move", data: action });
            },
            onMouseoutSquare: () => {
                hovering.forEach(h => getSquare(h).css("background", ""));
                hovering = [];
            },
            onMouseoverSquare: (pos) => {
                if (!state.moves) return;
                hovering = hovering.concat(state.moves.filter(s => s.startsWith(pos)).map(m => m.slice(2)));
                if (!hovering.length) return;
                hovering.push(pos);
                hovering.map(h => getSquare(h.slice(0, 2))).forEach(h => h.css("background", isDark(h) ? '#696969' : '#a9a9a9'));
            },
        });

        send({ type: "get_state" });
    }

    if (e.data.type === "play_move") {
        send({ type: "get_state" });
    }

    if (e.data.type === "error") {
        $("#error").html(e.data.data);
        send({ type: "get_state" });
    }

    if (e.data.type === "get_state") {
        state = e.data.data;
        board.position(state.current_fen, true);
        $("#history").text(state.history.map((v, i) => `${i+1}. ${v}`).join("\n"));
        $(".navbar").attr("class", "navbar navbar-expand-md " + (state.turn === "white" ? "bg-light" : "navbar-dark bg-black"));
    }
};