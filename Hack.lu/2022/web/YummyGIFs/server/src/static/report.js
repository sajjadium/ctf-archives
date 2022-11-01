async function onSubmit() {
  const reportForm = document.getElementById("report-form");
  const formData = new FormData(reportForm);
  const res = await fetch("/submitreport", { method: "POST", body: formData });
  const msg = await res.text();
  const alert = document.createElement("div");
  alert.textContent = msg;
  const footer = document.getElementById("footer");
  footer.replaceChildren(alert);
  if (res.ok) {
    alert.classList.add("alert", "alert-success");
  } else if (res.status === 503) {
    alert.classList.add("alert", "alert-error");
    alert.textContent = "Reporting service down 😫";
  } else {
    alert.classList.add("alert", "alert-error");
  }
  setTimeout(() => { footer.replaceChildren() }, 5000);
}