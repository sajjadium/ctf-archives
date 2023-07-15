function setLoadingStatus(text){
    $("#loader-text").text(text);
}

const sections = [
    "loader",
    "lobby",
    "question-tease",
    "question-answering",
    "answer-and-leaderboard"
]

function isolate(id){
    sections.forEach((section) => {
        if(section == id){
            // console.log("Show",section);
            $("#" + section).slideDown();
        }else{
            // console.log("Hide",section);
            $("#" + section).slideUp();
        }
    })
}

function formatTime(time){
    return (Math.floor(time / 60).toString().padStart(2, '0')) + ":" + ((time % 60).toString()).padStart(2, '0');
}

let howls = {};

function getSound(path){
    if(!howls[path]){
        howls[path] = new Howl({
            src: path.split(",")
        });
    }
    return howls[path];
}

let curMusic = null;
let curMusicPath = null;

function play(path){
    howls[path].play();
}

function ensureMusic(path){
    if(curMusicPath != path){
        if(curMusic){
            console.log("Fading",curMusicPath);
            howls[curMusicPath].fade(1.0, 0.0, 1000, curMusic);
        }
        curMusicPath = path;
        console.log("Playing",path);
        curMusic = howls[path].play();
        howls[curMusicPath].loop(true, curMusic);
        howls[curMusicPath].fade(0.0, 1.0, 1000, curMusic);
    }
}

const grey = "bg-slate-200";

const answerSlots = [
    "red",
    "blue",
    "yellow",
    "green"
]

let playerName = null;

$(function () {
    setLoadingStatus("Setting up realtime connection...");
    const socket = io();
    window.socket = socket; // for debugging!

    socket.once("connect", () => {
        setLoadingStatus("Connected...");
        $.toast("Connected to the server. ");
    });

    let phase = "loader";

    const colors = ["slate-100","slate-300"];

    function renderLobby(state){
        if(state.phaseState.startTime){
            $("#lobby-estimate").text("Starting in " + formatTime(Math.floor((state.phaseState.startTime - Date.now())/1000)))
        }else{
            $("#lobby-estimate").text("Waiting for server time estimate");
        }
        let playerList = $("#lobby-playerlist");
        playerList.empty();
        let index = 0;
        for(let player of state.players){
            let bgColor = colors[index % 2]; 
            playerList.append($("<div></div>").text(player.name).addClass("p-4 " + "bg-" + bgColor));
            index ++;
        }
        ensureMusic(state.sounds.lobby);
    }

    function renderGameplay(state){
        ensureMusic(state.sounds.gameplay);
    }

    function renderQuestionTease(state){
        renderGameplay(state);
        let phaseState = state.phaseState;
        let question = phaseState.question;
        let qText = $("#tease-question-text");
        let prevQuestionText = qText.text();
        if(prevQuestionText != question.text){
            qText.text(question.text);
            // TODO: render image
        }
        // slot fix
        $(".slot").removeClass(grey);
        $(".slot").each(function(){
            $(this).addClass($(this).attr("data-color-class"));
        })
        // text size thing
        let teaseEnd = phaseState.teaseEnd;
        let timeUntilTeaseEnd = teaseEnd - Date.now();
        let progress = (phaseState.teaseDuration - timeUntilTeaseEnd) / phaseState.teaseDuration;
        // 3xl 1.875rem
        let fontSizeRem = 1.875 + (progress * 1.5);
        qText.css("font-size", fontSizeRem + "rem");

        $(".slot").removeClass("grey");
    }

    function renderQuestionAnswering(state){
        renderGameplay(state);
        let phaseState = state.phaseState;
        let question = phaseState.question;
        let qText = $("#answering-question-text");
        let qImg = $("#answering-question-image")
        let prevQuestionText = qText.text();
        if(prevQuestionText != question.text){
            qText.text(question.text);
            if(question.image){
                qImg.show();
                qImg.attr("src", question.image);
            }else{
                qImg.hide();
            }

            for(let i = 0; i < answerSlots.length; i ++){
                const slot = answerSlots[i];
                const answerChoice = (phaseState.answers || [])[i];
                let slotEl = $("#" + slot);
                if(!answerChoice){
                    slotEl.hide();
                    slotEl.text("");
                    slotEl.removeClass(grey);
                } else{
                    slotEl.show();
                    slotEl.removeClass(grey);
                    slotEl.addClass(slotEl.attr("data-color-class"));
                    slotEl.text(answerChoice);
                }
            }
        }
        
        let questionEnd = phaseState.answeringEnd;
        let timeUntilQuestionEnd = questionEnd - Date.now();
        let progress = (phaseState.answeringDuration - timeUntilQuestionEnd) / phaseState.answeringDuration;
        $("#question-bar").css("width", (progress * 100) + "%");
        $("#question-bar").css("min-width", (progress * 100) + "%");
    }

    function renderReview(state){
        renderGameplay(state);

        let phaseState = state.phaseState;

        if(phaseState.question){
            let qText = $("#review-question");
            if(qText.text() != phaseState.question.text){
                qText.text(phaseState.question.text);
            }
        }
        if(phaseState.correctAnswer){
            let aText = $("#review-answer");
            if(aText.text() != phaseState.correctAnswer){
                aText.text(phaseState.correctAnswer);
            }
        }
    }

    function renderGameState(state){
        // ensure howls sfx exist
        Object.values(state.sounds).forEach(sound => getSound(sound));
        // phase change
        if(phase != state.phase){
            // console.log("Switching phase to ",state.phase);
            isolate(state.phase); // gui transfer
        }
        if(state.title && state.title != $("#header-text").text()){
            $("#header-text").text(state.title);
        }
        if(state.phase == "lobby"){
            renderLobby(state);
        }
        if(state.phase == "question-tease"){
            renderQuestionTease(state);
        }
        if(state.phase == "question-answering"){
            renderQuestionAnswering(state);
        }
        if(state.phase == "answer-and-leaderboard"){
            renderReview(state);
        }
        if(state.motd){
            $(".motd").text(state.motd);
        }else{
            $(".motd").text("Message of the day not set.");
        }
    }

    function onGameState(networkState){
        window.lastGameState = networkState;
        renderGameState(networkState);
    }

    socket.on("gameState", onGameState);

    socket.on("setName", (newName) => playerName = newName);

    function resyncGameState(){
        socket.emit("requestGameState");
    }

    socket.on("connect", () => {
        resyncGameState();
    });

    socket.on("systemMessage", (message, important = false) => {
        $.toast({
            text: message,
            icon: important ? "warning":"info",
            heading: "System Message",
            stack: 5,
           // position: "top-center",
            hideAfter: important ? 15*1000:5000
        });
        console.log("System message", message);
    });

    let outcomeEl = $("#review-outcome");

    socket.on("personalUpdate", (pState) => {
        $("#review-streak").text("You are on a streak of " + pState.streak);
        $("#review-points").text("You currently have " + pState.points + " pts. ");
        if(pState.correct){
            outcomeEl.addClass("bg-lime-500");
            outcomeEl.removeClass("bg-rose-500");
            outcomeEl.text("Correct!");
        }else{
            outcomeEl.removeClass("bg-lime-500");
            outcomeEl.addClass("bg-rose-500");
            outcomeEl.text("Wrong!");
        }
    });

    let lbEl = $("#leaderboard");
    socket.on("leaderboardUpdate", (lb) => {
        lbEl.empty();
        for(let player of lb){
            let nameDiv = $("<div></div>").text(player.name + " (streak: " + player.streak + ") ").addClass("flex-none");
            let growDiv = $("<div></div>").addClass("grow");
            let pointsDiv = $("<div></div>").text(player.points + " pts").addClass("flex-none");
            lbEl.append($("<div></div>").append(nameDiv).append(growDiv).append(pointsDiv).addClass("flex"));
        }
        let streaker = lb.reduce((a,b) => {
            if(a.streak > b.streak){
                return a;
            }
            return b;
        });
        $("#streak-stats").text("Out of " + lb.length + " total player(s), " + streaker.name + " has is on a streak of " + streaker.streak + " with " + streaker.points + " pts");
    });

    socket.on("disconnect", (_) => {
        $.toast({
            text: "We lost connection to the game server. You may not recieve flags! ",
            heading: "Oh no. ",
            icon: "error"
        });
    })

    $("#name-changer").on("change", function(ev){
        socket.emit("requestNameChange", $(this).val());
        resyncGameState();
    });

    let slots = $(".slot");

    slots.click(function(){
        const t = $(this);
        const choice = t.text();
        console.log("Submit",choice);
        const id = t.attr("id");
        if(!slots.hasClass(grey)){
            slots.each(function(){
                let self = $(this);
                if(id == self.attr("id")){
                    return;
                }
                self.removeClass($(self).attr("data-color-class"));
                self.addClass(grey);
            });
        }
        socket.emit("answerQuestion", choice);
    })

    // hack to fix latency for countdowns lmao
    
    function render(){
        if(window.lastGameState){
            renderGameState(window.lastGameState);
        }

        window.requestAnimationFrame(render);
    }

    window.requestAnimationFrame(render);
});