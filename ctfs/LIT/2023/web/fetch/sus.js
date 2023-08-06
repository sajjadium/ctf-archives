let alerted = false;
const observer = new MutationObserver((mutations) => {
  if (alerted) return;
  alert("Looks like you're getting somewhere!");
  alerted = true;
});

// Configure the observer with options
const options = {
  childList: true, // observe child node additions/deletions
  subtree: true, // observe changes in all descendant nodes
  attributes: true, // observe attribute changes
};

window.addEventListener("load", () => {
  // Attach the observer to a DOM element
  const targetNode = document.querySelector("#myElement");
  observer.observe(targetNode, options);
});

("big hints: headless browser with your file");
("gets flag from server");
("what can you do to intercept this?");
