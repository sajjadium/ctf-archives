import { Server } from "socket.io";
import { randomInt } from "crypto";
import { Question, GameState } from "../types";
import shuffleArray from "shuffle-array";
import express from "express";
import http from "http";
import path from "path";

const QUESTIONS: Question[] = [
  {
    question: "What color am I thinking of?",
    answers: ["Red", "Blue", "Yellow", "Green"],
    image: "https://upload.wikimedia.org/wikipedia/commons/0/04/Oil_painting_palette.jpg",
  },
  {
    question: "What prime number am I thinking of?",
    answers: ["2", "3", "5", "7"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Primes-vs-composites.svg/440px-Primes-vs-composites.svg.png",
  },
  {
    question: "What chord am I thinking of?",
    answers: ["Major", "Minor", "Diminished", "Augmented"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Frets%2C_guitar_neck%2C_C-major_chord.jpg/440px-Frets%2C_guitar_neck%2C_C-major_chord.jpg",
  },
  {
    question: "What angle am I thinking of?",
    answers: ["Acute", "Right", "Obtuse", "Straight"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Angle_obtuse_acute_straight.svg/600px-Angle_obtuse_acute_straight.svg.png",
  },
  {
    question: "What direction am I thinking of?",
    answers: ["North", "East", "South", "West"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Compass_Rose_English_North.svg/500px-Compass_Rose_English_North.svg.png",
  },
  {
    question: "What shape am I thinking of?",
    answers: ["Triangle", "Square at 45 degree angle", "Circle", "Square"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Polygon_types.svg/600px-Polygon_types.svg.png",
  },
  {
    question: "What element am I thinking of?",
    answers: ["Water", "Earth", "Fire", "Air"],
    image: "https://static1.srcdn.com/wordpress/wp-content/uploads/2020/07/Avatar-the-last-airbender-opening-credits.jpg",
  },
  {
    question: "What suit am I thinking of?",
    answers: ["Clubs", "Spades", "Hearts", "Diamonds"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/AcetoFive.JPG/440px-AcetoFive.JPG",
  },
  {
    question: "What string quartet part am I thinking of?",
    answers: ["Violin 1", "Violin 2", "Viola", "Cello"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Fitzwilliam_Quartet.jpg/580px-Fitzwilliam_Quartet.jpg",
  },
  {
    question: "What Beatle am I thinking of?",
    answers: ["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"],
    image: "https://upload.wikimedia.org/wikipedia/en/4/42/Beatles_-_Abbey_Road.jpg",
  },
  {
    question: "What operation am I thinking of?",
    answers: ["+", "-", "*", "/"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Basic_arithmetic_operators.svg/440px-Basic_arithmetic_operators.svg.png",
  },
  {
    question: "What season am I thinking of?",
    answers: ["Spring", "Summer", "Fall", "Winter"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/B%C3%A4ume_Jahreszeit_2013.jpg/520px-B%C3%A4ume_Jahreszeit_2013.jpg",
  },
  {
    question: "Which terrestrial planet am I thinking of?",
    answers: ["Mercury", "Venus", "Earth", "Mars"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Terrestrial_planet_sizes2.jpg/742px-Terrestrial_planet_sizes2.jpg",
  },
  {
    question: "Which gas giant am I thinking of?",
    answers: ["Jupiter", "Saturn", "Uranus", "Neptune"],
    image: "https://www.cnet.com/a/img/resize/617bcb1361018df5a09ba3bf3467e28faeb05fae/hub/2021/11/18/da0b5be7-0782-4563-b6e7-8d3381bd5621/stsci-01fm7r1qhaverq1tn0xz652605.jpg?auto=webp&fit=crop&height=675&width=1200",
  },
  {
    question: "Which DNA thing am I thinking of?",
    answers: ["Adenine", "Guanine", "Cytosine", "Thymine"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/DNA_Structure%2BKey%2BLabelled.pn_NoBB.png/680px-DNA_Structure%2BKey%2BLabelled.pn_NoBB.png",
  },
  {
    question: "Which blood type am I thinking of?",
    answers: ["A", "B", "O", "AB"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/ABO_blood_type.svg/870px-ABO_blood_type.svg.png",
  },
  {
    question: "Which state of matter am I thinking of?",
    answers: ["Solid", "Liquid", "Gas", "Plasma"],
    image: "https://www.physicsforums.com/attachments/phase_diagram-gif.92763/",
  },
  {
    question: "Which dimension am I thinking of?",
    answers: ["1st", "2nd", "3rd", "4th"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Squarecubetesseract.png/472px-Squarecubetesseract.png",
  },
  {
    question: "Which baseball base am I thinking of?",
    answers: ["First", "Second", "Third", "Home"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/DR_vs_PR._World_Baseball_Classic.jpg/440px-DR_vs_PR._World_Baseball_Classic.jpg"
  },
  {
    question: "Which violin string am I thinking of?",
    answers: ["E", "A", "D", "G"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Stainer.jpg/600px-Stainer.jpg",
  },
  {
    question: "Which moon of Jupiter visible from Earth am I thinking of?",
    answers: ["Io", "Europa", "Ganymede", "Callisto"],
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Jupiter_family.png/660px-Jupiter_family.png"
  },
  {
    question: "Which Fantastic Four am I thinking of?",
    answers: ["Mr. Fantastic", "The Invisible Woman", "The Human Torch", "The Thing"],
    image: "https://upload.wikimedia.org/wikipedia/en/1/1b/Fantastic_Four_%28Marvel_Comics_characters%29.jpg"
  },
  {
    question: "Which Teenage Mutant Ninja Turtle am I thinking of?",
    answers: ["Leonardo", "Michelangelo", "Donatello", "Raphael"],
    image: "https://upload.wikimedia.org/wikipedia/en/0/09/Teenage_Mutant_Ninja_Turtles_film_July_2014_poster.jpg",
  },
  {
    question: "Which limb am I thinking of?",
    answers: ["Right arm", "Left arm", "Right leg", "Left leg"],
    image: "https://media.gettyimages.com/id/129311937/photo/studio-shot-of-young-cheerful-man-with-arms-outstretched.jpg?s=612x612&w=gi&k=20&c=zkEGE6h2zBYADTEabXTCxKh9cxT1FwmSiiJ8A1PUHVg=",
  },
  {
    question: "Which house am I thinking of?",
    answers: ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"],
    image: "https://static1.moviewebimages.com/wordpress/wp-content/uploads/2022/06/Hogwarts-Houses-(1).jpg",
  },
];

async function main(io: Server) {
  let scoreboard: Record<string, number> = {};
  let answered = new Set();
  let questionIndex = 0;
  let correctAnswer = randomInt(4);
  let answerRevealed = false;
  let sleepEndTime: number = 0;

  function sleep(seconds: number) {
    sleepEndTime = new Date().getTime() + 1000 * seconds;
    return new Promise((resolve) => setTimeout(resolve, 1000 * seconds));
  }

  function gameState(): GameState {
    return {
      question: QUESTIONS[questionIndex],
      questionIndex,
      scoreboard,
      correctAnswer: answerRevealed ? correctAnswer : undefined,
      timeLeft: 8000,
    };
  }

  io.on("connect", socket => {
    socket.emit("gameState", { ...gameState(), timeLeft: sleepEndTime - new Date().getTime() });
    socket.on("answer", (answer: number) => {
      if (answered.has(socket.id) || answerRevealed) {
        return;
      }
      answered.add(socket.id);
      if (!(socket.id in scoreboard)) {
        scoreboard[socket.id] = 0;
      }
      if (answer == correctAnswer) {
        scoreboard[socket.id] += 1;
      } else {
        scoreboard[socket.id] = 0;
      }
      if (scoreboard[socket.id] >= 21) {
        socket.emit("flag", process.env.FLAG ?? "bctf{fake_flag}");
      }
    })
  })

  while (true) {
    if (questionIndex === 0) {
      shuffleArray(QUESTIONS);
    }
    answerRevealed = false;
    answered.clear();
    correctAnswer = randomInt(4);
    io.emit("gameState", gameState());
    await sleep(8);
    answerRevealed = true;
    for (const player of Object.keys(scoreboard)) {
      if (!answered.has(player)) {
        delete scoreboard[player];
      }
    }
    io.emit("gameState", gameState());
    await sleep(3);
    questionIndex = (questionIndex + 1) % QUESTIONS.length;
  }
}

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static(path.join(__dirname, "../client/dist")));

main(io);

server.listen(1024);