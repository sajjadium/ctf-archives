const START_POS = "8/8/8/8/8/8/PPPPPPPP/RNBQKBNR";

let state = {};
let moveSnd = new Audio("mp3/move.mp3");
let board;
let hover;
let chat = [];

const restart = () => {
    location.reload();
};

const hoverColors = {
    light: '#a9a9a9',
    dark: '#696969'
};

const fogColors = {
    light: '#4C4C4C',
    dark: '#212121'
};

const noColor = {
    light: "",
    dark: ""
};

const colorSquare = (pos, { light, dark }) => {
    let square = $('#chessboard .square-' + pos);
    let isDark = square.hasClass('black-3c85d');
    square.css("background", isDark ? dark : light);
};

const render = () => {
    let pos = board.position();
    let hovered = [];

    if(hover) {
        let moves = state.moves.filter(s => s.startsWith(hover));
        if (moves.length !== 0) {
            hovered.push(hover);
            for (let i = 0; i < moves.length; i++) {
                hovered.push(moves[i].slice(2));
            }
        }
    }

    for(let r of "abcdefgh") {
        for(let c of "12345678") {
            let sq = r+c;
            if(hovered.includes(sq) && !state.game_over) {
                colorSquare(sq, hoverColors);
            }
            else if(!state.moves.some(s => s.endsWith(sq))
                && !pos[sq]
                && !state.game_over
                && !state.pawn_attacks.includes(sq)) {
                colorSquare(sq, fogColors);
            }
            else {
                colorSquare(sq, noColor);
            }
        }
    }

    if(state.your_turn) {
        $("nav").addClass("bg-primary");
        $("nav").removeClass("bg-danger")
        $("#turn").text("Your Turn");
    }
    else {
        $("nav").addClass("bg-danger");
        $("nav").removeClass("bg-primary");
        $("#turn").text("Opponent Turn");
    }

    let msges = chat.map(c => `${c.name}: ` + c.msg.replace(/</g, "&lt;").replace(/>/g, "&gt;")).join("<br />");
    $("#chat").html(msges);
};

const move = (action) => {
    if(!state.moves.includes(action))
        action += "q"; // force promotion to queen

    socket.emit("move", action);
    moveSnd.play();
};

const onDragStart = (source, piece) => {
    if(!state.your_turn || state.game_over || !state.moves.some(s => s.startsWith(source)))
        return false;
};

const onDrop = (source, target) => {
    let action = `${source}${target}`;
    if(!state.moves.includes(action) && !state.moves.includes(action + "q")) // promotion
        return "snapback";
    move(action);
};

const onMouseoverSquare = (square) => {
    hover = square;
};
const onMouseoutSquare = () => {
    hover = null;
};

let socket = io();
socket.on('connect', () => {
    console.log("connected");
});
socket.on('disconnect', () => {
    chat.push({name: "System", msg: "Lost connection to the game server, please restart"})
});

socket.on('chat', (msg) => {
    chat.push(msg);
    chat = chat.slice(-15);
});

socket.on('state', (data) => {
    if(!board) {
        board = Chessboard('chessboard', {
            draggable: true,
            position: data.pos,
            onDragStart,
            onDrop,
            onMouseoutSquare,
            onMouseoverSquare,
        });

        setInterval(() => {
            render();
        }, 25);
    }
    else {
        if(data.your_turn && !state.your_turn) {
            moveSnd.play();
        }
        board.position(data.pos, false);
    }
    state = data;
});