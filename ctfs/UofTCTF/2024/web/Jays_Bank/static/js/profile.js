document.addEventListener("DOMContentLoaded", function () {
  const profileForm = document.getElementById("profileForm");
  const changePasswordForm = document.getElementById("changePasswordForm");
  const messageBox = document.getElementById("messageBox");

  function showMessage(message, isSuccess = true) {
    messageBox.textContent = message;
    messageBox.style.display = "block";
    messageBox.className = isSuccess ? "success" : "error"; 
  }


  function hideMessage() {
    messageBox.style.display = "none";
  }

  profileForm.addEventListener("submit", function (e) {
    e.preventDefault();
    hideMessage();

    const formData = new FormData(profileForm);
    const data = {};
    formData.forEach((value, key) => (data[key] = value));

    fetch("/profile", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((json) => {
        showMessage(json.message, json.success);
      })
      .catch((err) => showMessage(err.toString(), false));
  });

  if (changePasswordForm) {
    changePasswordForm.addEventListener("submit", function (e) {
      e.preventDefault();
      hideMessage();


      const formData = new FormData(changePasswordForm);
      const data = {};
      formData.forEach((value, key) => (data[key] = value));


      fetch("/change_password", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((json) => {
          showMessage(json.message, json.success);
        })
        .catch((err) => showMessage(err.toString(), false));
    });
  }
});
