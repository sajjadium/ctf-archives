import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";
import { GameState } from "../../types";

export default function App() {
  const [state, setState] = useState<GameState>();
  const [socket, setSocket] = useState<Socket>();
  const [answered, setAnswered] = useState<number | undefined>(undefined);

  useEffect(() => {
    const socket = io();
    setSocket(socket);
    socket.on("flag", (flag) => {
      alert(flag);
    });
    socket.on("gameState", (state: GameState) => {
      if (state.correctAnswer === undefined) {
        setAnswered(undefined);
      }
      setState(state);
    });
    return () => {
      socket.disconnect();
    };
  }, []);

  if (!state || !socket) {
    return;
  }

  const sendAnswer = (answer: number) => {
    socket.emit("answer", answer);
    setAnswered(answer);
  };

  let [bestPlayer, bestScore] = ["nobody", 0];
  for (const [player, score] of Object.entries(state.scoreboard)) {
    if (score > bestScore) {
      bestScore = score;
      bestPlayer = player;
    }
  }

  const shapes = ["▲", "◆", "⬤", "■"];
  const colors = ["bg-red-500", "bg-blue-500", "bg-yellow-500", "bg-green-500"];

  return (
    <div className="grid grid-rows-[min-content_1fr_2fr_1fr] bg-gray-100 h-[100vh] p-4 gap-4 relative">
      <div className="flex flex-row justify-between">
        <div>
          You: {socket.id} &mdash; {state.scoreboard[socket.id] ?? 0} / 21
        </div>
        <div>
          Best: {bestPlayer} &mdash; {bestScore} / 21
        </div>
      </div>
      <div className="bg-white shadow-md text-xl flex flex-col">
        <div
          className="bg-blue-500 h-4"
          style={{
            animation:
              state.correctAnswer === undefined ? `progress 8s linear` : "none",
            animationDelay: `${state.timeLeft - 8000}ms`,
          }}
        ></div>
        <div className="m-auto">{state.question.question}</div>
      </div>
      <div className="bg-center bg-contain bg-no-repeat drop-shadow-md" style={{
        backgroundImage: `url(${state.question.image})`
      }}>
      </div>

      {state.correctAnswer !== undefined && (
        <div className="absolute left-[50%] -translate-x-1/2 top-[50%] -translate-y-1/2 shadow-lg">
          <div>
            {state.correctAnswer === answered && (
              <div className="bg-green-400 w-[40em] h-[6em] text-black p-4 grid place-items-center">
                <div>Correct!</div>
              </div>
            )}
            {state.correctAnswer !== answered && (
              <div className="bg-red-400 w-[40em] h-[8em] text-black p-4 gap-2 flex flex-row content-center items-center">
                <div>
                  {answered !== undefined ? "Incorrect!" : "Out of time!"} The
                  correct answer was
                </div>
                <div
                  className={`p-4 flex-1 -translate-y-1 text-white ${colors[state.correctAnswer]
                    } flex flex-row gap-4 items-center shadow-md`}
                >
                  <div className="text-xl">{shapes[state.correctAnswer]}</div>{" "}
                  {state.question.answers[state.correctAnswer]}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        {state.question.answers.map((answer, i) => (
          <button
            className={`shadow-md p-8 text-white text-left flex flex-row gap-4 items-center
          ${colors[i]} ${answered !== undefined && answered !== i ? "opacity-50" : ""
              } ${answered === undefined ? "hover:opacity-90" : ""}`}
            disabled={
              answered !== undefined || state.correctAnswer !== undefined
            }
            onClick={() => sendAnswer(i)}
          >
            <div className="text-4xl -translate-y-1">{shapes[i]}</div>{" "}
            <div>{answer}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
