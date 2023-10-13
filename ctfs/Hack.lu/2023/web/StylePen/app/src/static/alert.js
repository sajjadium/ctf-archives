document.querySelector(".close-button")?.addEventListener("click", () => {
    document.querySelector(".alert-container").classList.add("hidden");
})

function showAlert(message, type) {
    const alertContainer = document.querySelector(".alert-container");
    alertContainer.classList.remove("hidden");
    alertContainer.classList.add(type);
    alertContainer.querySelector(".alert-message").innerText = message;
}