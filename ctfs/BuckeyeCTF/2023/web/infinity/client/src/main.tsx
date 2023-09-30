import React from "react";
import ReactDOM from "react-dom/client";
import { IoProvider } from "socket.io-react-hook";
import "./index.css";
import StartButton from "./StartButton.tsx";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <IoProvider>
      <StartButton />
    </IoProvider>
  </React.StrictMode>,
);
