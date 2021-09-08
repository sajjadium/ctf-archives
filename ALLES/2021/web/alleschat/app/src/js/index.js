const slogans = [
  "Four out of Five Dentists Recommend <strong>ALLES!Chat</strong>.",
  "<strong>ALLES!Chat</strong>. Making people sucessful in a changing world.",
  "If Only Everything in Life was as Reliable as <strong>ALLES!Chat</strong>.",
  "Life's beautiful with <strong>ALLES!Chat</strong>.",
  "<strong>ALLES!Chat</strong> - Probably The Best Messaging App In The World.",
  "A Day Without <strong>ALLES!Chat</strong> is Like a Day Without Sunshine.",
  "So Easy, No Wonder <strong>ALLES!Chat</strong> is #1.",
  "When The Going Gets Tough, The Tough Get <strong>ALLES!Chat</strong>.",
  "8 out of 10 Owners who Expressed a Preference said Their Cats Preferred <strong>ALLES!Chat</strong>.",
  "<strong>ALLES!Chat</strong> - a safe place in an unsafe world!",
];
const socket = createSocket();

socket.on("newMessage", (data) => {
  receivedNewMessage(data);

  document.getElementById("message-counter").innerText++;
});

window.onload = () => {
  if (!token) {
    window.location.href = "./login.html";
    return;
  }

  document.getElementById("greeting").innerText = "Welcome Back, " + username;
  document.getElementById("slogan").innerHTML =
    slogans[Math.floor(Math.random() * slogans.length)];

  socket.emit("contacts");
};
