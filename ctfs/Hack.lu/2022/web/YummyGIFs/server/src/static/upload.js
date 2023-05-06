const uploadForm = document.getElementById("upload-form");
const uploadProgress = document.getElementById("upload-progress");
uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!uploadForm.reportValidity()) return;
  uploadProgress.classList.remove("hidden");
  const formData = new FormData(uploadForm);
  const ajax = new XMLHttpRequest();
  ajax.upload.addEventListener("progress", (e) => {
    const percent = (e.loaded / e.total) * 100;
    uploadProgress.value = Math.round(percent);
  });
  ajax.addEventListener("load", (e) => {
    if (e.target.status === 200) {
      window.location = `/view.php?id=${encodeURIComponent(e.target.responseText)}&success=Successful+file+upload!`;
    } else {
      uploadProgress.classList.add("hidden");
      const alert = document.createElement("div");
      alert.textContent = e.target.responseText;
      const footer = document.getElementById("footer");
      footer.replaceChildren(alert);
      alert.classList.add("alert", "alert-error");
    }
    setTimeout(() => footer.replaceChildren(), 5000);
  });
  ajax.open("POST", "/upload.php");
  ajax.send(formData);
});