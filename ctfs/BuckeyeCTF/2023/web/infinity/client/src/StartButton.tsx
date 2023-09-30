import { useRef, useState } from "react";
import App from "./App";

export default function StartButton() {
    const audio = useRef<HTMLAudioElement | null>(null);
    const [started, setStarted] = useState(false);

    return <>
        <audio ref={audio} loop>
            <source src="https://ia903101.us.archive.org/24/items/KahootLobbyMusic/Kahoot%20Lobby%20Music%20%28HD%29.mp3"></source>
        </audio>
        {!started && <div className="gradient h-full w-full flex flex-col gap-8 items-center justify-center -rotate-45 scale-[200%]">
            <div className="text-6xl text-white drop-shadow-md">
                <span className="text-8xl translate-y-[10px] inline-block">∞</span><span className="font-bold">!</span>
            </div>
            <button onClick={() => {
                audio.current?.play();
                setStarted(true);
            }} className="text-4xl text-white hover:scale-110 transition-all backdrop-brightness-110 hover:backdrop-brightness-125 p-4 shadow-md">PLAY</button>
        </div>}
        {started && <App />}
    </>
}