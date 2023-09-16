const wrap = (obj) =>
  new Proxy(obj, {
    get: (target, prop) => {
      const res = target[prop];
      return typeof res === "function" ? res.bind(target) : res;
    },
    set: (target, prop, value) => (target[prop] = value),
  });

const $ = wrap(document).querySelector;

const sandboxAttribute = [
  "allow-downloads",
  "allow-forms",
  "allow-modals",
  "allow-orientation-lock",
  "allow-pointer-lock",
  "allow-popups",
  "allow-popups-to-escape-sandbox",
  "allow-presentation",
  "allow-same-origin",
  // "allow-scripts", // disallow
  "allow-top-navigation",
  "allow-top-navigation-by-user-activation",
  "allow-top-navigation-to-custom-protocols",
].join(" ");

const createBlink = async (html) => {
  const sandbox = wrap(
    $("#viewer").appendChild(document.createElement("iframe"))
  );

  // I believe it is impossible to escape this iframe sandbox...
  sandbox.sandbox = sandboxAttribute;

  sandbox.width = "100%";
  sandbox.srcdoc = html;
  await new Promise((resolve) => (sandbox.onload = resolve));

  const target = wrap(sandbox.contentDocument.body);
  target.popover = "manual";
  const id = setInterval(target.togglePopover, 400);

  return () => {
    clearInterval(id);
    sandbox.remove();
  };
};

$("#render").addEventListener("click", async () => {
  const html = $("#html").value;
  if (!html) return;
  location.hash = html;

  const deleteBlink = await createBlink(html);
  const button = wrap(
    $("#viewer").appendChild(document.createElement("button"))
  );
  button.textContent = "Delete";
  button.addEventListener("click", () => {
    deleteBlink();
    button.remove();
  });
});

const initialHtml = decodeURIComponent(location.hash.slice(1));
if (initialHtml) {
  $("#html").value = initialHtml;
  $("#render").click();
}
