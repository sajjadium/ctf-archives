console.log("App started")

const makeRequest = (route) => {
    const RELapi = document.getElementById("api").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const error = document.getElementById("error");
  
    if (!RELapi || !username || !password) return;
  
    fetch(RELapi + route, {
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
  
        localStorage.setItem("api", new URL(RELapi).origin);
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
    let RELapi = localStorage.getItem("api");
    if (RELapi) document.getElementById("api").value = RELapi;
  };
  