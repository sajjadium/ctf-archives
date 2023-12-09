// Set forms to use json
$(document).ready(() => {
  $("form").submit((event) => {
    event.preventDefault();

    const data = Object.fromEntries(new FormData(event.target).entries());
    $.ajax({
      type: "POST",
      url: event.target.getAttribute("action"),
      contentType: "application/json",
      data: JSON.stringify(data),
      success: (data) => {
        // Handle the response from the server
        if (data.redirect) window.location.pathname = data.redirect;
        if (data.message) window.messagebox.innerText = data.message;
      },
      error: (error) => {
        console.error("Error:", error);
        window.messagebox.className = "alert alert-danger";
        window.messagebox_heading.innerText = "Failure!";
        window.messagebox_content.innerText =
          "Error occured.. We're doing our best to provide you the best CTF experience.";
        window.messagebox.removeAttribute("hidden");
      },
    });
  });
});
