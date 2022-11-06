function login() {
  const username = document.querySelector("#username").value;
  const password = document.querySelector("#password").value;
  fetch("/api/login", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ username, password }).toString(),
  }).then(x => x.json()).then(x => {
    if (!x.ok) {
      document.querySelector(".alert").textContent = x.message
      document.querySelector(".alert").classList.remove("d-none");
    } else {
      location.href = "/";
    }
  });
}

document.querySelector("#login").addEventListener('click',login);