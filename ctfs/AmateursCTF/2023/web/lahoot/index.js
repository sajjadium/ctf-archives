import http, { get } from "http";
import express from "express";
import {Server} from "socket.io";

import {init, Player} from "./db.js";

import config from "./config.js";

import generate from "./name.js"

import crypto from "crypto";
import { secureShuffle } from "./utils.js";

import {config as config2} from "dotenv";
config2();

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const port = process.env.PORT || 3000;

// flavor: instance specific customizations!
app.use(express.static("flavor"));
app.use(express.static("public"));
app.get("/", (req,res) => res.sendFile("public/index.html"));

// Game logic!
let curPhase = "lobby";

let socketIDToName = new Map(); 
let playerState = new Map();
let gottenItCorrect = new Set();
let currentQuestionRoundIndex = 0;
let currentQuestionPrivate = null;

function sleep(ms){
  return new Promise((resolve,reject) => setTimeout(resolve,ms));
}

let state = {};

async function getState(){
  let sockets = await io.sockets.fetchSockets();
  return {
    phase: curPhase,
    phaseState: state,
    players: sockets.map((socket) => {
      return {
        name: socketIDToName.get(socket.id) 
      }
    }),
    title: config.title,
    sounds: {
      lobby: config.lobby_music,
      gameplay: config.gameplay_music
    },
    motd: config.motd
  }
}

async function syncLeaderboardsToPublic(){
  let playerRanking = [];
  let sockets = await io.sockets.fetchSockets();
  for(let socket of sockets){
    let pState = getPlayerState(socket.id);
    playerRanking.push({
      name: socketIDToName.get(socket.id),
      points: pState.points,
      streak: pState.streak
    });
  }
  playerRanking.sort((a,b) => b.points - a.points);
  state.playerRanking = playerRanking;
  io.emit("leaderboardUpdate", playerRanking);
}

function getPlayerState(id){
  if(!playerState.has(id)){
    playerState.set(id, {
      points: 0,
      streak: 0
    });
  }
  return playerState.get(id);
}

async function resetGame(){
  await Player.sync({
    force: true
  }); // drop previous data
  playerState.clear();
  await syncLeaderboardsToPublic();
}

async function lobby(){
    curPhase = "lobby";
    io.emit("systemMessage", "Starting Lobby for a new game. ");
    const duration = config["lobby_time"];
    state.startTime = Date.now() + duration;
    await sleep(duration);
    delete state.startTime;
    io.emit("systemMessage", "Time is up, starting game.");
}

async function presentQuestion(question){
  gottenItCorrect.clear();
  currentQuestionPrivate = question;
  // tease
  curPhase = "question-tease";
  state.question = question.question; // show only text and optional image
  const teaseDuration = question.teaseTime || config.teaseTime || 15 * 1000;
  state.teaseEnd = Date.now() + teaseDuration;
  state.teaseDuration = teaseDuration;
  console.log("Teasing", question.question);
  await sleep(teaseDuration);
  // answer!
  curPhase = "question-answering";
  delete state.teaseEnd;
  delete state.teaseDuration;
  
  // reveal possible answers after a shuffle
  const correctIndex = question.correctIndex || 0;
  const correctAnswer = question.answers[correctIndex]
  state.answers = secureShuffle([...question.answers]);
  state.answeringStart = Date.now();

  const answeringDuration = question.answeingTime || config.answeringTime || 15 * 1000;
  state.answeringEnd = Date.now() + answeringDuration;
  state.answeringDuration = answeringDuration;
  await sleep(answeringDuration);

  delete state.answeringStart;
  delete state.answeringEnd;
  delete state.answeringDuration;
  delete state.answers;

  // Compose leaderboard update
  curPhase = "answer-and-leaderboard"
  state.correctAnswer = correctAnswer;

  let sockets = await io.sockets.fetchSockets();
  for(let socket of sockets){
    let pState = getPlayerState(socket.id);
    if(gottenItCorrect.has(socket.id)){
      pState.streak ++;
    }else{
      pState.streak = 0;
    }
    socket.emit("personalUpdate", {
      ...pState,
      correct: gottenItCorrect.has(socket.id)
    });
    playerState.set(socket.id, pState);
  }
  await syncLeaderboardsToPublic();

  let reviewDuration = question.reviewTime || config.reviewTime || (3 * 1000);
  state.reviewStart = Date.now();
  state.reviewDuration = reviewDuration;
  state.reviewEnd = Date.now() + reviewDuration;
  await sleep(reviewDuration);
  delete state.correctAnswer;
  delete state.reviewStart;
  delete state.reviewDuration;
  delete state.reviewEnd;
  delete state.question;
  // keep going
}

async function gameEnd(){
  // pick winners and send flag
  // io.sockets.sockets.get(
}

io.on("connection", (socket) => {
    socketIDToName.set(socket.id, generate());
    socket.emit("setName", socketIDToName.get(socket.id));
    socket.on("requestGameState", async () => {
      socket.emit("gameState",await getState());
    });
    socket.on("requestNameChange", (newName) => {
      if(newName){
        if(curPhase != "lobby"){
          return;
        }
        if(newName.length >= 3 && newName.length < 24){
          socketIDToName.set(socket.id, newName);
          socket.emit("setName", socketIDToName.get(socket.id));
        }else{
          socket.emit("systemMessage", "When selecting a name, please ensure it as at least 3 characters and less than 24 characters. ");
        }
      }
    });

    socket.on("answerQuestion", async (choice) => {
      if(curPhase != "question-answering"){
        socket.emit("systemMessage", "Question is not open to answer anymore! Sorry. ");
        return;
      }
      let [player, created] = await Player.findOrCreate({
          where: {
            id: socket.id
          },
          defaults: {
            lastSubmitIndex: -1 // players can join midgame
          }
      });
      if(player.lastSubmitIndex < currentQuestionRoundIndex){
        const correctIndex = currentQuestionPrivate.correctIndex || 0;
        const correctAnswer = currentQuestionPrivate.answers[correctIndex];
        console.log(correctAnswer, choice);
        if(correctAnswer == choice){
          const decay = currentQuestionPrivate.decaying_time || config.decaying_time || (10 * 1000);
          const questionPoints = currentQuestionPrivate.points || config.points;
          const offset = config.offset; // offset extra few points for lag
          const points = Math.min(Math.max(0, Math.floor(((Date.now() - (state.answeringStart || 0))/(decay)) * questionPoints)) + offset, questionPoints)

          let playerState = getPlayerState(socket.id);
          playerState.points += points;

          gottenItCorrect.add(socket.id);
        }else{
          // sad no points oof
        }
        player.lastSubmitIndex = currentQuestionRoundIndex;
        await player.save();
      }else{
        socket.emit("systemMessage", "You already submitted an answer to this question. ");
      }
    });

    socket.emit("systemMessage", "System is in test mode");
});

setInterval(async () => {
  io.emit("gameState",await getState());
}, 100);

init().then(async () => {
  console.log("Initalized databases...");
  
  server.listen(port, () => {
    console.log(`Server is up on port ${port}!!!`);
  });

  // Game loop

  while(true){
    await lobby();
    await resetGame();
    currentQuestionRoundIndex = 0;
    for(let r = 0; r < config.round_distribution.length; r ++){
      let seenQuestions = new Set();
      for(let i = 0; i < config.round_distribution[r]; i ++){
        let chosenQuestionIndex = crypto.randomInt(config.questions[r].length);
        let tries = 0; // TODO: delete tries logic, might keep it in for testing
        while(seenQuestions.has(chosenQuestionIndex)){
          chosenQuestionIndex = crypto.randomInt(config.questions[r].length);
          tries ++;
          if(tries > 1000){
            break;
          }
        }
        seenQuestions.add(chosenQuestionIndex);
        currentQuestionRoundIndex ++;

        let chosenQuestion = config.questions[r][chosenQuestionIndex];

        await presentQuestion(chosenQuestion);
      }
    }
    let sockets = await io.sockets.fetchSockets();
    let total = config.round_distribution.reduce((a,b) => a + b);
    for(let socket of sockets){
      if(playerState.get(socket.id).streak >= total){
        // player is cracked so we give flag.
        socket.emit("systemMessage",process.env.FLAG || "amateursCTF{t3st3ing_and_d3v3lop3m3nt_fl@g}",true);
      }else{
        socket.emit("systemMessage", "Did you know? High streak players will get an exclusive flag. Sadly you only had a streak of " + playerState.get(socket.id).streak + " but we require " + total)
      }
    }
  }
});