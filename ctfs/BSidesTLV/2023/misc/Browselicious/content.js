// Listen for messages from the extension
window.addEventListener("message", function (event) {
    // Check if the message is from the extension
    if (event.source === window && event.data.action === "populatePassword") {
        // Find the password input field
        var passwordField = document.querySelector('input[type="password"]');

        // Populate the password field with the specified string
        if (passwordField) {
            passwordField.value = (event.data.url === "http://flag") ? "BSidevTLV2023{TheFlag}" : "MyDefaultPassword";
        }
    }
});

// Send a message to populate the password field on page load
window.addEventListener("load", function () {
    window.postMessage({
        action: "populatePassword",
        url: window.location.href,
        password: "YourPassword" // Replace with the desired password
    }, "*");
});
