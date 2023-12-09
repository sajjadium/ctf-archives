const sendAction = async (action) => {
  window.messagebox.setAttribute("hidden", true);
  window.messagebox_heading.innerText = "";
  window.messagebox_content.innerText = "";
  window.messagebox_image.setAttribute("hidden", true);

  const result = await fetch(`/api/actions/${action}`);
  if (!result.ok) {
    window.messagebox.className = "alert alert-danger";
    window.messagebox_heading.innerText = "Failure!";
    window.messagebox_content.innerText =
      "Something went wrong :( *sad robotic noises*";
    window.messagebox.removeAttribute("hidden");
    return;
  }

  window.messagebox_heading.innerText = "Success!";
  window.messagebox.className = "alert alert-success text-center";
  if (result.headers.get("Content-Type").startsWith("application/json")) {
    const data = await result.json();
    if (data.result === "success") {
      window.messagebox_content.innerText = "Robot has moved! bzz bzz";
    } else {
      console.error({ msg: "bro what", data });
    }
  } else {
    const img = await result.blob();
    window.messagebox_image.src = URL.createObjectURL(img);
    window.messagebox_content.innerText = "Click click!";
    window.messagebox_image.removeAttribute("hidden");
  }
  window.messagebox.removeAttribute("hidden");
};
const buyAction = async (action) => {
  const result = $.ajax({
    type: "POST",
    url: "/buy",
    contentType: "application/json",
    data: JSON.stringify({
      item: action,
    }),
    success: (data) => {
      // Handle the response from the server
      console.log('ok', {data});
      if (data.redirect) window.location.pathname = data.redirect;
      if (data.message) window.messagebox.innerText = data.message;
    },
    error: (error) => {
      console.error("Error:", error);
      window.messagebox.className = "alert alert-danger";
      window.messagebox_heading.innerText = "Failure!";
      window.messagebox_content.innerText =
        "Cannot buy the item";
        window.messagebox.removeAttribute("hidden");
      },
    
  });
};
