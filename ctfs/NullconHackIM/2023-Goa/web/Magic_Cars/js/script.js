
function toggleChat() {
    const chatBox = document.getElementById("chat-box");
    chatBox.style.display = chatBox.style.display === "none" ? "block" : "none";
}


function addMessage(message) {
const chatMessages = document.getElementById("chat-messages");
const newMessage = document.createElement("p");
newMessage.textContent = message;
chatMessages.appendChild(newMessage);
chatMessages.scrollTop = chatMessages.scrollHeight; 
setTimeout(() => {
    chatMessages.removeChild(newMessage);
}, 10000);
}

function sendMessage() {
    const message = document.getElementById("chat-input").value.trim();
    if (message !== "") {
    addMessage("You: " + message);
    saveMessage("You: " + message);
    document.getElementById("chat-input").value = "";
    }
}

function saveMessage(message) {
    const existingMessages = JSON.parse(localStorage.getItem("chat_messages")) || [];
    existingMessages.push(message);
    localStorage.setItem("chat_messages", JSON.stringify(existingMessages));
}

function loadMessages() {
    const existingMessages = JSON.parse(localStorage.getItem("chat_messages")) || [];
    existingMessages.forEach((message) => {
    addMessage(message);
    });
}

loadMessages();


document.getElementById("send-button").addEventListener("click", sendMessage);


document.getElementById("chat-input").addEventListener("keyup", (event) => {
    if (event.keyCode === 13) {
    sendMessage();
    }
});

function toggleContent(selectedTab) {
    const contentSections = document.getElementsByClassName("content");
    for (let i = 0; i < contentSections.length; i++) {
    contentSections[i].style.display = "none";
    }

    const selectedContent = document.getElementById(selectedTab);
    selectedContent.style.display = "block";
}


function toggleUploadForm() {
    const uploadForm = document.getElementById("gallery-upload-form");
    uploadForm.style.display = uploadForm.style.display === "none" ? "block" : "none";
}
