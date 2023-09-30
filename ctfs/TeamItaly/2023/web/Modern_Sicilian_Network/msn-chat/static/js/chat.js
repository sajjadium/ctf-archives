var SPACES_PORT = 6969; // default value, will be eventually updated later
const PARENT_DOMAIN = location.hostname.substring(location.hostname.indexOf('.')+1);
const EMOTICONS = {
	":tofu:": "/static/propic/tofu.png",
	":)": "/static/style/assets/chat-window/412.png",
	";)": "/static/style/assets/chat-window/1487.png"
}

const chatWindow = document.querySelector('.mainwindow#chat');
const messagesContainer = document.querySelector('.chattext#display');
const chatInput = document.querySelector('textarea');
const sendButton = document.querySelector('#send-button');
const nudgeButton = document.querySelector('#nudge-button');
const searchButton = document.querySelector('#search');

const profileUsername = document.querySelector('.user-info #username');
const profilePropic = document.querySelector('.user-info #avatar');
const profilePropicChat = document.querySelector('#bottomavatar .avatar');

const recipientUsername = document.querySelector('#recipient-info #recipient-name');
const recipientStatus = document.querySelector('#recipient-info #recipient-message');
const recipientPropic = document.querySelector('#topavatar .avatar');
const recipientBusyAlert = document.querySelector('#busy-alert');
const recipientBusyAlertText = document.querySelector('#busy-alert .alert-text');

const spacesMenuButton = document.querySelector('#spaces-button');
const spacesMenu = document.querySelector('#spaces-menu');
const spacesArticles = document.querySelector('#spaces-articles');

const emoticonsMenuButton = document.querySelector('#emoticons-button');
const emoticonsMenu = document.querySelector('#emoticons-menu');
const emoticonButtons = document.querySelectorAll('#emoticons-panel img');

const soundNudge = document.querySelector('#sound-nudge');
const soundType = document.querySelector('#sound-type');
soundType.volume = 0.4;

var profile = undefined;
var chatOpened = false;

var socket = undefined;
var renderedMessages = [];
var recipient = undefined;

var lastMessageBy = undefined;
var lastMessageType = undefined;
var lastArticleRefresh = 0;

var powDone = false;
var powSolution = undefined;

fetch('/api/v1/session').then(r => r.json()).then(json => {
	profile = json;
	profileUsername.textContent = profile.username;
	profilePropic.src = profile.propic;
	profilePropicChat.src = profile.propic;
});
fetch('/api/v1/spacesPort').then(r => r.text()).then(port => SPACES_PORT = port);

window.onload = () => {
	let match = window.location.pathname.match(
		/^\/chat\/([0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12})/i
	);
	if (match !== null) {
		loadChat(match[1]);
		chatInput.focus();
	} else {
		messagesContainer.innerHTML = '<span style="color: red">Please provide an user.</span>';
	}
};

sendButton.onclick = (event) => {
	event.preventDefault();
	const message = chatInput.value.trim();
	if (message.length === 0)
		return;
	sendMessage(0, message);
	chatInput.value = '';
};

nudgeButton.onclick = sendNudge;

spacesMenuButton.onmouseover = () => {
	spacesMenuButton.classList.add("active");
	// wait 4 seconds before refresh
	if (Date.now() - lastArticleRefresh > 4000)
		loadArticles(profile.id);
};
spacesMenuButton.onmouseout = () => {
	spacesMenuButton.classList.remove("active");
}

emoticonsMenuButton.onmouseover = () => emoticonsMenuButton.classList.add("active");
emoticonsMenuButton.onmouseout = () => emoticonsMenuButton.classList.remove("active");
emoticonButtons.forEach(btn => {
	btn.onclick = typeEmoticon;
});

searchButton.onclick = (event) => {
	event.preventDefault();
	searchMessage(recipient.id);
}

chatInput.onkeydown = (event) => {
	if (event.key === 'Enter' && !event.shiftKey && !event.ctrlKey) {
		const message = chatInput.value.trim();
		if (message.length === 0)
			return;
		event.preventDefault();
		sendMessage(0, message);
		chatInput.value = '';
	}
};
chatInput.onkeyup = (event) => {
	sendButton.disabled = chatInput.value.length == 0
}

// to be implemented correctly
function openChat(userId) {
	history.pushState(null, null, `/chat/${userId}`);
	loadChat(userId);
}

async function loadChat(userId) {
	if (userId === recipient?.id)
		return;

	if (socket)
		socket.disconnect();

	const res = await fetch(`/api/v1/users/${userId}`);
	if (!res.ok) {
		messagesContainer.innerHTML = '<span style="color: red">This user does not exist.</span>';
		chatOpened = false;
		recipient = undefined;
		return;
	}
	recipient = await res.json();
	messagesContainer.innerHTML = '';
	recipientUsername.textContent = recipient.username;
	recipientPropic.src = recipient.propic;
	renderedMessages = [];

	socket = io();
	socket.emit('join', userId);
	socket.on('message', (data) => {
		data.messages.forEach(renderMessage);
		chatOpened = true;
	});
	socket.on('nudge', renderNudge);
	socket.on('pow', launchBackgroundPow)
	recipientStatus.innerHTML = recipient.username == 'Loldemort' ? 'probably eating an arancina' : 'Having fun with Team Italy!';
	recipientBusyAlert.style.display = recipient.username == 'Loldemort' ? 'flex' : 'none';
}

function sendMessage(type, content) {
	socket.emit('message', type, content);
}

function renderMessage(message) {
	const { id, type, content, sender } = message;
	if (renderedMessages.find((e) => e === id) !== undefined) {
		return;
	}
	renderedMessages.push(id);

	if (type == 0) {
		// normal message
		if (lastMessageBy !== sender || lastMessageType != 0) {
			const messageHeader = document.createElement('span');
			messageHeader.classList = 'sender';
			username = (sender == profile.id) ? profile.username : recipient.username;
			messageHeader.textContent = `${username} says:`;
			messagesContainer.appendChild(messageHeader);
		}
		const messageText = document.createElement('span');
		messageText.classList = 'message';
		messageText.textContent = content;
		messageText.dataset.id = id;
		// render emoticons
		messageText.innerHTML = messageText.innerHTML.replace(/:\)|;\)|:tofu:/g, m => `<img src="${EMOTICONS[m]}" class="emoticon" />`);
		messagesContainer.appendChild(messageText);
	} else if (type == 1) {
		// article
		const messageHeader = document.createElement('span');
		messageHeader.classList = 'sender';
		username = (sender == profile.id) ? profile.username : recipient.username;
		messageHeader.textContent = `${username} sent an article:`;
		messagesContainer.appendChild(messageHeader);
		const articleLink = document.createElement('a');
		articleLink.href = `//spaces.${PARENT_DOMAIN}:${SPACES_PORT}/articles/${content}`;
		articleLink.target = '_blank';
		articleLink.textContent = 'Loading...';
		articleLink.dataset.article = content;
		renderArticle(articleLink);
		const articleWrapper = document.createElement('span'); // !
		articleWrapper.classList = 'message';
		articleWrapper.appendChild(articleLink);
		messagesContainer.appendChild(articleWrapper);
	}
	lastMessageBy = sender;
	lastMessageType = type;
	if(profile.id !== sender) {
		if(chatOpened)
			soundType.play();
	}
	scrollChatToBottom();
}

function sendNudge(event) {
	event.preventDefault();
	if (powDone !== true) {
		renderNudge(false);
		return;
	}
	powDone = false;
	socket.emit('nudge', powSolution);
}

function renderNudge(event) {
	// this is to let people play with the nudge while browser calculates PoW
	var fakeNudge = false;
	if (event === false) {
		event = { sender: profile.id };
		fakeNudge = true;
	}

	lastMessageBy = undefined;
	const { sender } = event;
	soundNudge.currentTime = 0;
	soundNudge.play();
	const nudgeText = document.createElement('span');
	nudgeText.classList = 'nudge';
	username = (sender == profile.id) ? profile.username : recipient.username;
	nudgeText.textContent = fakeNudge ? "Your nudge wasn't delivered. PoW is still being calculated." : `${username} sent a nudge.`;
	messagesContainer.appendChild(nudgeText);
	chatWindow.classList.add('is-nudged');
  	setTimeout(() => chatWindow.classList.remove('is-nudged'), 450);
	scrollChatToBottom();
}

function scrollChatToBottom() {
	setTimeout(() => {
		messagesContainer.scrollTop = messagesContainer.scrollHeight;
	}, 50);
}

function typeEmoticon(event) {
	const [start, end] = [chatInput.selectionStart, chatInput.selectionEnd];
  	chatInput.setRangeText(` ${event.target.dataset.emoticon}`, start, end, 'select');
}

function sendArticle(event) {
	socket.emit('message', 1, event.target.dataset.article);
}

async function renderArticle(element) {
	articleRef = element.dataset.article;
	const res = await fetch(`//spaces.${PARENT_DOMAIN}:${SPACES_PORT}/api/v1/articles/${articleRef}`);
	if (!res.ok) {
		element.textContent = "(error while loading the title)";
		return;
	}
	article = await res.json();
	element.textContent = article.title;
}

async function loadArticles(userId) {
	const res = await fetch(`//spaces.${PARENT_DOMAIN}:${SPACES_PORT}/api/v1/articles/${userId}`);
	if (!res.ok) {
		spacesArticles.innerHTML = '<li style="color: red">Server error.</li>';
	}
	articles = await res.json();
	if (articles.length == 0) {
		spacesArticles.innerHTML = 'No articles found.';
		return;
	}
	spacesArticles.innerHTML = '';
	articles.forEach(article => {
		articleElement = document.createElement('li');

		articleTitle = document.createElement('a');
		articleTitle.textContent = article.title;
		articleTitle.classList = 'article-title';
		articleTitle.onclick = sendArticle;
		articleTitle.dataset.article = `${userId}/${article.id}`;
		articleElement.appendChild(articleTitle);

		articlePreview = document.createElement('p');
		articlePreview.textContent = article.content.replace( /(<([^>]+)>)/ig, '').substring(0, 50); // strip ugly HTML tags away
		articleElement.appendChild(articlePreview);

		spacesArticles.appendChild(articleElement);
	});
	lastArticleRefresh = Date.now();
}

async function searchMessage(userId) {
	query = prompt("What do you want to search for? (case-sensitive)", "");
	document.querySelectorAll(".highlighted").forEach(e => e.classList.remove("highlighted"));
	if (!query || query.length == 0)
		return;
	res = await fetch(`/api/v1/search/${userId}?query=` + encodeURIComponent(query));
	if (!res.ok) {
		alert("No messages found.");
		return;
	}
	list = await res.json();
	list.forEach(id => { console.log(id); document.querySelector(`[data-id="${id}"]`).classList.add("highlighted"); });
	alert(`Found ${list.length} messages.`);
}

async function launchBackgroundPow(pow) {
	powDone = false;
	nudgeButton.style.filter = "grayscale(1)";
	const { target, complexity } = pow;
	powSolution = await window.solvePow(target, complexity);
	powDone = true;
	nudgeButton.style.filter = "grayscale(0)";
}