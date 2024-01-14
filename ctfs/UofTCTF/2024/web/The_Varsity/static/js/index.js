function requestArticle() {
  const articleNum = document.getElementById("articleNum").value;
  const statusMessage = document.getElementById("statusMessage");
  const articlesDiv = document.getElementById("articles");

  fetch("/article", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ issue: articleNum }),
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((err) => {
          throw err;
        });
      }
      return response.json();
    })
    .then((article) => {
      if (articlesDiv && statusMessage) {
        articlesDiv.innerHTML = `<h2>${article.title}</h2><p>${article.content}</p>`;
        statusMessage.textContent = "Enjoy reading!";
      }
    })
    .catch((error) => {
      if (statusMessage) {
        statusMessage.textContent = "Couldn't load article!";

        articlesDiv.innerHTML = error.message || "Unknown error";
      }
      console.error("Error:", error);
    });
}
