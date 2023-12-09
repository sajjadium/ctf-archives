const resetOwnership = (action_id) => {
  $.ajax({
    type: "POST",
    url: "/admin",
    contentType: "application/json",
    data: JSON.stringify({
      id: action_id,
    }),
    success: (data) => {
      // Handle the response from the server
      if (data.redirect) window.location.pathname = data.redirect;
      if (data.message) window.messagebox.innerText = data.message;
    },
    error: (error) => {
      console.error("Error:", error);
    },
  });
};
