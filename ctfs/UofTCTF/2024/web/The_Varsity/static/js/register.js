function toggleVoucher() {
  const voucherGroup = document.getElementById("voucherGroup");
  voucherGroup.style.display = document.getElementById("hasVoucher").checked
    ? "block"
    : "none";
}

document.getElementById("registrationForm").onsubmit = function (event) {
  event.preventDefault();
  const username = document.getElementById("username").value;
  const voucher = document.getElementById("hasVoucher").checked
    ? document.getElementById("voucher").value
    : "";

  fetch("/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, voucher }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === "Invalid voucher") {
        document.getElementById("feedback").textContent = data.message;
      } else {
        document.cookie = `token=${data.token};path=/`;
        window.location.href = "/";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};
