const makeRequest = (route) => {
  const api = document.getElementById("api").value;
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const error = document.getElementById("error");

  if (!api || !username || !password) return;

  fetch(api + route, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  })
    .then((data) => data.json())
    .then((data) => {
      if (data["error"]) {
        error.innerText = data["error"];
        error.classList.remove("is-hidden");
        setTimeout(() => {
          error.classList.add("is-hidden");
        }, 2500);
        return;
      }

      localStorage.setItem("api", new URL(api).origin);
      localStorage.setItem("username", username);
      localStorage.setItem("token", data["token"]);
      window.location.href = "./index.html";
    })
    .catch((err) => {
      error.innerText = err;
      error.classList.remove("is-hidden");
      setTimeout(() => {
        error.classList.add("is-hidden");
      }, 2500);
    });
};

document.getElementById("register").addEventListener("click", () => {
  makeRequest("/register");
});
document.getElementById("login").addEventListener("click", () => {
  makeRequest("/login");
});

window.onload = () => {
  let api = localStorage.getItem("api");
  if (api) document.getElementById("api").value = api;
};
