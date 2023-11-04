
  const socket = io();
  socket.on("status", (data) => {
      if (data == "auth") {
          cookies = document.cookie
          tokenIndex = cookies.indexOf("token=")+"token=".length
          token = cookies.substr(tokenIndex,32)
          socket.emit("auth",token);
      }
  });
  
  socket.on("notifications", (data) => {
    notifCount.innerText = "("+data.length+")"
    if (data.length == 0) {
        return
    }
    notificationsList.innerHTML = ""
    notifHTML = ""
    for (let i = 0; i < data.length; i++) {
        notifHTML += `<li>${data[i]}</li>`
    }
    notificationsList.innerHTML = DOMPurify.sanitize(notifHTML)
    preview.innerHTML = DOMPurify.sanitize("("+data[data.length-1]+"...)")
  });