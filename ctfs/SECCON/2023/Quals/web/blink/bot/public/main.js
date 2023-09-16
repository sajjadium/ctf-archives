const $ = document.getElementById.bind(document);

$("appUrl").textContent = await fetch("/app-url").then((r) => r.text());

let loading = false;
$("report").addEventListener("click", async () => {
  if (loading) return;
  const url = $("url").value;
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    alert("Invalid url");
    return;
  }

  loading = true;
  $("report").toggleAttribute("disabled");
  $("report").setAttribute("aria-busy", "true");
  $("report").textContent = "";

  const res = await fetch("/api/report", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url }),
  });
  if (res.status === 200) {
    alert("Completed!");
  } else {
    alert(await res.text());
  }

  loading = false;
  $("report").toggleAttribute("disabled");
  $("report").setAttribute("aria-busy", "false");
  $("report").textContent = "Report";
});
