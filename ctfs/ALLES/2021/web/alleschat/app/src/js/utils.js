const api = localStorage.getItem("api");
const token = localStorage.getItem("token");
const username = localStorage.getItem("username");

const makeNotification = (title, body) => {
  window.postMessage({ type: "notification", title: title, body: body });
};

const writeLog = (level, msg) => {
  window.postMessage({ type: "logging", level: level, msg: msg });
};

const createContactLi = (user) => {
  let a = document.createElement("a");
  a.setAttribute("href", `./chat.html?user=${encodeURIComponent(user)}`);
  a.setAttribute("id", user);
  a.innerText = user.substring(0, 15);
  if (user.length > 15) a.innerText += "...";

  let li = document.createElement("li");
  li.appendChild(a);

  return li;
};

const receivedNewMessage = (data) => {
  let users = document.getElementById("users");

  if (data["sender"] === username && data["recipient"] !== data["sender"])
    return;

  if (!document.getElementById(data["sender"]))
    // add sender to latest messages
    users.insertBefore(
      createContactLi(data["sender"]),
      users.firstElementChild
    );

  if (data["sender"] === username) return;

  if (
    !document
      .getElementById(data["sender"])
      .classList.contains("has-text-weight-bold")
  )
    document
      .getElementById(data["sender"])
      .classList.add("has-text-weight-bold");

  makeNotification(`New Message From ${data["sender"]}`, data["message"]);
};

const createSocket = () => {
  const socket = io(api, { auth: { token: token }, reconnectionAttemps: 3 });

  socket.on("connect_error", (err) => {
    writeLog("error", err.message);

    if (err.message === "Invalid token") {
      // invalid token, redirect to login
      localStorage.removeItem("token");
      window.location.href = "./index.html";
    }
  });

  socket.on("contacts", (data) => {
    let users = document.getElementById("users");

    for (let i = 0; i < 3 && i < data["contacts"].length; i++) {
      let contact = data["contacts"][i];
      if (contact === "support") continue;

      users.appendChild(createContactLi(contact));
    }
  });

  window.addEventListener("beforeunload", () => {
    socket.disconnect();
  });

  return socket;
};

window.onerror = (err) => {
  writeLog("error", err);
};
