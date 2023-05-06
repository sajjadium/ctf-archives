(() => {
    let chats = Object.create(null);
    let current;
    let $ = document.querySelector.bind(document); // imagine using jQuery

    const register = async () => {
        const { value: username } = await Swal.fire({
            title: 'Enter a username:',
            icon: 'info',
            input: 'text',
            inputPlaceholder: 'username',
            allowOutsideClick: false,
            inputValidator: (value) => {
              if (!value) {
                return 'Please enter a username'
              }
            }
        });

        if(!username) {
            return register();
        }

        let r = await fetch("/chat/login", {
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: `name=${encodeURIComponent(username)}`
        });
        let resp = await r.json();
        if(!resp.success) {
            await Swal.fire("Error", 'There was an error with that username.', 'error');
        }
        location.reload();
    }

    const sandbox = (code) => {
        return new Promise((resolve, reject) => {
            try {
                let iframe = document.createElement("iframe");
                let token = (+new Date * Math.random()).toString(36).substring(0,6);
                iframe.src = "/sandbox";
                iframe.sandbox = "allow-scripts";
                iframe.style.display = "none";
                iframe.onload = () => {
                    iframe.contentWindow.postMessage({ code, token }, "*");
                }
                window.onmessage = (e) => {
                    if(e.data.token !== token) {
                        return;
                    }

                    window.onmessage = null;
                    resolve(e.data.res);
                }
                setTimeout(() => iframe?.remove(), 1500);
                document.body.appendChild(iframe);
            }
            catch(err) {
                iframe?.remove();
                resolve("Error");
            }
        });
    };

    const filter = (msg) => {
        if(typeof msg !== "string") {
            msg = "[ERROR]";
        }
        if(msg.toLowerCase().includes("corctf{")) {
            msg = "[REDACTED]"; // no flags for you!!!!!!
        }
        return msg;
    };

    const sideChatRoom = (name) => {
        let li = document.createElement("li"), a = document.createElement("a");
        a.onclick = () => { current = name; render(); }
        a.innerText = name;
        if(current === name) {
            a.innerText = "> " + a.innerText;
        }
        li.appendChild(a);
        $("#chats").appendChild(li);
    };
    
    const newMessage = async (msg) => {
        let li = document.createElement("li");

        let name = msg.from;
        if(msg.from == username) {
            li.className = "own";
        }
        if(msg.system) {
            name = "system";
            li.className = "system";
        }

        let sender = document.createElement("div");
        sender.className = "sender";
        sender.innerText = name;

        let content = document.createElement("div");
        content.className = "content";

        if(msg.type === "sandbox") {
            let code = msg.msg.split(":").slice(1).join(":");
            msg.type = null;
            msg.msg = `${name}: ${await sandbox(code)}`;
            render();
            return;
        }
        else {
            content.innerHTML = filter(msg.msg);
        }

        li.appendChild(sender);
        li.appendChild(content);

        $("#messages").appendChild(li);
    };

    const render = () => {
        if(Object.keys(chats).length === 0) {
            $("#chat").style.display = "none";
            return;
        }
        
        $("#chat").style.display = "grid";
        $("#messages").textContent = "";
        $("#chats").textContent = "";

        Object.keys(chats).forEach(name => sideChatRoom(name));
        if(current) {
            chats[current].forEach(m => newMessage(m));
            $("#messages").scrollTop = $("#messages").scrollHeight;
        }
    };

    let username = $("#username").innerText;
    if(!username) {
        return register();
    }

    let ws = new WebSocket(location.origin.replace("https://", "wss://").replace("http://", "ws://") + "/chat/ws");
    ws.onopen = () => {
        ws.onmessage = (e) => {
            let data = JSON.parse(e.data);

            if(!data.from) {
                return;
            }
            if(!chats[data.from]) {
                chats[data.from] = [];
            }
            if(data.from === username && !data.system) {
                return;
            }

            chats[data.from].push(data);
            render();
        }

        let qs = new URLSearchParams(location.search.substring(1));
        if(qs.get("from")) {
            let from = qs.get("from");
            if(!chats[from]) {
                chats[from] = [];
            }
            current = from;
            render();
        }
    };
    ws.onclose = async () => {
        await Swal.fire("Error", 'Lost connection to the server.', 'error');
        location.reload();
    };

    $("#new-chatroom-form").addEventListener("submit", (event) => {
        event.preventDefault();
        if(!username) {
            return;
        }
        let userInput = $("#new-chatroom-user");
        if (userInput.value && !chats[userInput.value]) {
            chats[userInput.value] = [];
            current = userInput.value;
        }
        userInput.value = "";
        render();
    });

    $('#msg-form').addEventListener('submit', async (e) => {
        event.preventDefault();
        if(!username) {
            return;
        }
        let textInput = $("#msg");
        if (textInput.value) {
            chats[current].push({ to: current, from: username, msg: textInput.value });
            await fetch("/chat/send", {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: `to=${encodeURIComponent(current)}&msg=${encodeURIComponent(textInput.value)}`
            });
        }
        textInput.value = "";
        render();
    });
})();