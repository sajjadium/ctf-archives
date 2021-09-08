const socket = createSocket();

const sendMessage = () => {
  let recipient = document.getElementById("recipient").value;
  let message = document.getElementById("new-message").value;

  if (recipient.length > 0 && message.length > 0) {
    socket.emit("sendMessage", { message: message, recipient: recipient });
    window.location.href = `./chat.html?user=${encodeURIComponent(recipient)}`;
  }
};

socket.on("newMessage", (data) => {
  receivedNewMessage(data);
});

window.onload = () => {
  socket.emit("contacts");

  document.getElementById("send").addEventListener("click", sendMessage);
  document.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
};
