const $ = document.querySelector.bind(document); // imagine using jQuery...

const DENYLIST = ["__proto__", "constructor", "prototype"]; // no
const parseQs = () => {
  let obj = {};
  let pairs = location.search.slice(1).split('&').filter(Boolean);
  for (let i = 0; i < pairs.length; i++) {
    if (DENYLIST.some(key => pairs[i].includes(key))) continue;

    let parts = pairs[i].split('=');
    let m;
    if (m = /(\w+)\[(\w+)\]/.exec(decodeURIComponent(parts[0]))) {
      obj[m[1]] = obj[m[1]] || [];
      obj[m[1]][m[2]] = decodeURIComponent(parts[1]);
    } else {
      obj[decodeURIComponent(parts[0])] = decodeURIComponent(parts[1]);
    }
  }

  history.pushState(null, null, location.pathname);
  return obj;
};
let qs = parseQs();

const graphql = async (query, variables) => {
  let r;
  if (variables) {
    r = await fetch("/graphql", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        query,
        variables
      })
    });
  } else {
    r = await fetch("/graphql?query=" + encodeURIComponent(query), {
      credentials: "same-origin"
    });
  }
  return await r.json();
};

window.onload = async () => {
  if (qs.message) {
    alert(qs.message);
    await new Promise(r => setTimeout(r, 500));
  }
  qs = null;

  let res = await graphql(`query { info { money, isAdmin } }`);
  if (res.errors) {
    // not logged in
    $("#anonymous").style.display = "block";
  } else {
    // welcome!
    let { money, isAdmin } = res.data.info;
    $("#user").style.display = "block";
    $("#money").innerText = `Money: $${money}`;

    if (isAdmin) {
      // enable WIP contacts feature
      let res = await graphql(`query { info { contacts } }`);
      if (res.errors || !res.data.info.contacts) return;
      let html = `<h3>contacts:</h3><ol>`;
      res.data.info.contacts.forEach(user =>
        html += `<li onclick="transferToUser('${user}')" style="cursor:pointer">${user}</li>`
      );
      html += `</ol>`;
      $("#contacts").innerHTML = html;
    }
  }
};

$("#authform").addEventListener("submit", (e) => {
  e.preventDefault();
  login();
});

const login = async () => {
  let username = $("input[name=username]").value;
  let password = $("input[name=password]").value;

  let res = await graphql(`
        mutation($username: String!, $password: String!) { 
          login(username: $username, password: $password) { 
            username 
          } 
        }
        `, {
    username,
    password
  });

  if (res.errors) {
    location.href = '/?message=' + encodeURIComponent(res.errors[0].message);
  } else {
    location.href = '/?message=' + encodeURIComponent(`logged in as ${res.data.login.username}`);
  }
};

const register = async () => {
  let username = $("input[name=username]").value;
  let password = $("input[name=password]").value;

  let res = await graphql(`
        mutation($username: String!, $password: String!) { 
          register(username: $username, password: $password) { 
            username 
          } 
        }
        `, {
    username,
    password
  });

  if (res.errors) {
    location.href = '/?message=' + encodeURIComponent(res.errors[0].message);
  } else {
    location.href = '/?message=' + encodeURIComponent(`registered as ${res.data.register.username}`);
  }
};

const deposit = () => {
  location.href = '/?message=' + encodeURIComponent("sorry, this functionality is not implemented yet");
};

const transfer = () => {
  const to = prompt("enter recipient's username:");
  if (!to) return;
  transferToUser(to);
};

const transferToUser = async (recipient) => {
  let amount = prompt(`how much do you want to transfer to ${recipient}?`);
  if (!amount) return;
  amount = parseInt(amount);
  if (isNaN(amount)) return;

  let res = await graphql(`
        mutation($recipient: String!, $amount: Int!) { 
          transfer(recipient: $recipient, amount: $amount) { 
            money 
          } 
        }
        `, {
    recipient,
    amount
  });

  if (res.errors) {
    location.href = '/?message=' + encodeURIComponent(res.errors[0].message);
  } else {
    let { money } = res.data.transfer;
    location.href = '/?message=' + encodeURIComponent(`transfered $${amount} to ${recipient}, new balance: $${money}`);
  }
};

const logout = async () => {
  let res = await graphql(`
        mutation { 
          logout
        }
      `, {});
  if (res.errors) {
    location.href = '/?message=' + encodeURIComponent(res.errors[0].message);
  } else {
    location.href = '/?message=' + encodeURIComponent(`logged out succesfully`);
  }
};