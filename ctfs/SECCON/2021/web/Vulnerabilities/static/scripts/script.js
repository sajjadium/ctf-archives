document.addEventListener("DOMContentLoaded", async e => {
  const name = document.getElementById("name");
  const error = document.getElementById("error");
  const logo = document.getElementById("logo");
  const url = document.getElementById("url");

  //  Update logo and URL
  const update = async () => {
    name.disabled = true;
    try {
      const response = await fetch("/api/vulnerability", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "Name": name.value,
        })
      });
      if (!response.ok) {
        throw new Error(response.statusText);
      }

      const data = await response.json();
      if (data.Error) {
        throw new Error(data.Error);
      }

      logo.src = data.Logo;
      url.href = data.URL;
      url.textContent = data.URL;

      error.textContent = "";
      error.style.display = "none";
    } catch (err) {
      error.textContent = `Error: ${err.message}`;
      error.style.display = "block";
    } finally {
      name.disabled = false;
      name.focus();
    }
  };

  name.addEventListener("change", update);

  //  Retrieve a list of vulnerabilities
  try {
    const response = await fetch("/api/vulnerabilities");
    if (!response.ok) {
      throw new Error(response.statusText);
    }

    const data = await response.json();
    if (data.Error) {
      throw new Error(data.Error);
    }

    for (const vulnerability of data.Vulnerabilities) {
      const option = document.createElement("option");
      option.value = vulnerability;
      option.textContent = vulnerability;
      name.appendChild(option);
    }
    await update();
  } catch (err) {
    error.textContent = `Error: ${err.message}`;
    error.style.display = "block";
  }
});
