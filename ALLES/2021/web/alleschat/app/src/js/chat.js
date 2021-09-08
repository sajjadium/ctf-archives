const user = new URLSearchParams(location.search).get("user");
const socket = createSocket();

const makeLinks = (text) => {
  text
    .match(/(https?|mailto|file):[\w\/\?\&\.\=\%\#\:\-]+(\s|$)/gi)
    ?.forEach((link) => {
      link = link.trim();
      let a = document.createElement("a");
      a.href = link;
      a.innerText = link;

      text = text.replace(link, a.outerHTML);
    });

  return text;
};

const createChatMessage = (msg) => {
  // turn links into a tags
  msg["message"] = makeLinks(msg["message"]);

  let strong = document.createElement("strong");
  strong.innerText = msg["sender"] === username ? "You" : msg["sender"];

  let a = document.createElement("a");
  a.classList.add("ml-6");
  a.innerText = "Print This Message";
  a.href = `${api}/print?id=${msg["id"]}&token=${token}&auto=1`;

  let small = document.createElement("small");
  small.classList.add("ml-5");
  small.innerText = new Date(msg["time"]).toLocaleString();
  small.appendChild(a);

  let p = document.createElement("p");
  p.classList.add("msg");
  p.appendChild(strong);
  p.appendChild(small);
  p.innerHTML += "<br />" + DOMPurify.sanitize(msg["message"]) + "<br />";

  if (window.isDev) {
    // make sure the a tags have a valid href attribute
    let links = Array.from(p.getElementsByTagName("a")).filter(
      (link) => link.href && /^(https?|file|mailto):$/.test(link.protocol)
    );
    links.shift(); // remove "Print This Message" link

    if (links.length > 0) {
      let link = new URL(links.pop());

      if (link.hostname.endsWith(".youtube.com"))
        link = "https://www.youtube.com/embed/" + link.searchParams.get("v");

      let iframe = document.createElement("iframe");
      iframe.sandbox = "allow-scripts allow-same-origin"; // safety first
      iframe.src = link;
      iframe.classList.add("preview", "mt-3");

      p.appendChild(iframe);
    }
  }

  let divContent = document.createElement("div");
  divContent.classList.add("content");
  divContent.appendChild(p);

  let divMedia = document.createElement("div");
  divMedia.classList.add("media-content");
  divMedia.appendChild(divContent);

  let article = document.createElement("article");
  article.classList.add("media");
  article.appendChild(divMedia);

  document.getElementById("messages").appendChild(article);
};

socket.on("newMessage", (data) => {
  receivedNewMessage(data);

  if (data["sender"] === user || data["recipient"] === user)
    createChatMessage(data);

  let div = document.getElementById("messages");
  div.scrollTop = div.scrollHeight;
});

socket.on("getMessages", (data) => {
  for (let msg of data["messages"]) {
    createChatMessage(msg);
  }

  let div = document.getElementById("messages");
  div.scrollTop = div.scrollHeight;

  document.getElementById(user)?.classList.add("is-active");

  if (user === "support")
    document.getElementById("support").classList.add("is-active");
});

const sendMessage = () => {
  let message = document.getElementById("new-message");
  if (message.value.length === 0) return;

  socket.emit("sendMessage", { message: message.value, recipient: user });

  message.value = "";
  message.focus();

  let div = document.getElementById("messages");
  div.scrollTop = div.scrollHeight;
};

window.onload = () => {
  if (!user) return;

  document.getElementById("user").innerText = user;

  socket.emit("contacts");
  socket.emit("getMessages", { user: user });

  document.getElementById("send").addEventListener("click", sendMessage);
  document.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
};
