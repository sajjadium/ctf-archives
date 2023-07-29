// sorry for the spaghetti

const moveSnd = new Audio("/mp3/move.mp3");
const socket = io();

let state = {}, hovering = [], chat = [];

const getSquare = (sq) => $('#chessboard .square-' + sq);
const isDark = (sq) => sq.hasClass('black-3c85d');
const restart = () => location.reload();
const htmlEscape = (d) => d.replace(/</g, "&lt;").replace(/>/g, "&gt;");

socket.on('connect', () => {
    console.log("connected");
});

socket.on('disconnect', () => {
    chat.push({ name: "System", msg: "Lost connection to the game server, please restart" })
});

socket.on('chat', (msg) => {
    chat.push(msg);
    chat = chat.slice(-15);
    $("#chat").html(chat.map(c => `${htmlEscape(c.name)}: ${htmlEscape(c.msg)}`).join("<br />"));
});

socket.on('state', (data) => {
    state = data;
    board.position(state.pos, true);
    moveSnd.play();
    $(".navbar").attr("class", "navbar navbar-expand-md " + (state.your_turn ? "bg-primary" : "bg-danger"));
    $("#turn").text(`${state.your_turn ? "Your" : "Computer"} Turn (${state.turn_counter})`);
    $(".row-5277c > div").css("background", "");
    if (data.status !== "running") {
        setTimeout(() => {
            $(".navbar").attr("class", "navbar navbar-expand-md bg-info");
            if (data.status === "draw") {
                Swal.fire({
                    title: 'Draw!',
                    icon: 'info'
                });
                $("#turn").text(`Draw! (${state.turn_counter})`);
            }
            else if (data.status === "turn limit") {
                Swal.fire({
                    title: 'Out of turns!',
                    icon: 'info'
                });
                $("#turn").text(`Out of turns! (${state.turn_counter})`);
            }
            else {
                Swal.fire({
                    title: 'Checkmate!',
                    iconColor: state.your_turn ? 'red' : 'green',
                    icon: 'info'
                });
                $("#turn").text(`Checkmate - ${state.your_turn ? 'Black' : 'White'} Win! (${state.turn_counter})`);
            }
        }, 500);
    }
});

const board = Chessboard('chessboard', {
    draggable: true,
    position: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    onDragStart: (source) => state.moves.some(s => s.startsWith(source)),
    onDrop: (source, target) => {
        let action = `${source}${target}`;
        // check if move exists, or move exists with promotion to queen
        if (!state.moves.includes(action) && !state.moves.includes(action + "q"))
            return "snapback";
        // if move is a promotion move, ask what piece to promote to
        (async () => {
            if (!state.moves.includes(action)) { // promotion
                const { value: promotion } = await Swal.fire({
                    title: 'What do you want to promote to?',
                    input: 'select',
                    inputOptions: {
                        'q': 'Queen',
                        'n': 'Knight',
                        'b': 'Bishop',
                        'r': 'Rook'
                    },
                    icon: 'question',
                });
                action += promotion;
            }
            moveSnd.play();
            state.moves = [];
            socket.emit("move", action);
        })();
    },
    onMouseoutSquare: () => {
        $(".row-5277c > div").css("background", "");
        hovering = [];
    },
    onMouseoverSquare: (pos) => {
        if (!state.moves || state.status !== "running") return;
        hovering = hovering.concat(state.moves.filter(s => s.startsWith(pos)).map(m => m.slice(2)));
        if (!hovering.length) return;
        hovering.push(pos);
        hovering.map(h => getSquare(h.slice(0, 2))).forEach(h => h.css("background", isDark(h) ? '#696969' : '#a9a9a9'));
    },
});