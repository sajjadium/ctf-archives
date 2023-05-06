const { ipcRenderer } = require("electron");

// Our remote networking setup is a bit different, therefore:
//  - remote default api: http://127.0.0.1:1024
//  - local api when running with docker: http://api:1024
const apiUrl =
  localStorage.getItem("api") ||
  (process.env.BROKERSESSIONID ? "http://127.0.0.1:1024" : "http://api:1024");

let counter = 0;

const makeNotification = (title, body) => {
  ipcRenderer.send("notification", ++counter);
  new Notification(title, { body: body });
};

const writeLog = (level, msg) => {
  ipcRenderer.send("logging", level, msg);
};

const isDev = () => {
  window.postMessage({
    isDev: process.env.NODE_ENV === "development",
  });
};

window.addEventListener("message", (e) => {
  if (
    (e.origin !== "file://" && e.origin !== apiUrl) ||
    typeof e.data !== "object"
  )
    return;

  switch (e.data.type) {
    case "notification":
      makeNotification(e.data.title, e.data.body);
      break;

    case "logging":
      writeLog(e.data.level, e.data.msg);
      break;

    case "isDev":
      isDev();
      break;
  }
});

window.isDev = process.env.NODE_ENV === "development";

// auto login for support bot
if (
  process.env.BOT === "1" &&
  window.location.href.endsWith("login.html") &&
  !localStorage.getItem("token")
) {
  let password = Array.from(crypto.getRandomValues(new Uint8Array(16)))
    .map((r) => r.toString(16))
    .join("");

  writeLog("info", "Logging in as support with password: " + password);

  fetch(`${apiUrl}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: "support",
      password: password,
    }),
  })
    .then((data) => data.json())
    .then((data) => {
      localStorage.setItem("api", apiUrl);
      localStorage.setItem("username", "support");
      localStorage.setItem("token", data["token"]);

      window.location.href = "./chat.html?user=support";
    })
    .catch((error) => {
      writeLog("error", error);
    });
}
