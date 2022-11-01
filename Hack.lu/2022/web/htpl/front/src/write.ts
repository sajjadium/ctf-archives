import { createEditor } from "./editor";

const shareLink = document.querySelector<HTMLAnchorElement>("#share-link")!;
function save(code: string) {
  const hash = window.btoa(code);
  location.hash = hash;
  shareLink.hash = hash;
}

function load() {
  return (
    window.atob(location.hash.slice(1)) || `<x-program>\n    \n</x-program>`
  );
}

function run() {
  document
    .querySelectorAll<HTMLElement>("#code .run-btn")
    .forEach((el) => el.click());
}

function render(code: string) {
  document.querySelector<HTMLElement>("#code")!.innerHTML = code;
}

async function main() {
  const container = document.getElementById("editor");
  if (!container) return;
  const code = load();
  save(code);
  render(code);

  const { onChange, onRun } = await createEditor(container, code);

  onChange((code) => {
    save(code);
    render(code);
  });

  onRun(run);
}
(window as any).run = run;
window.addEventListener("DOMContentLoaded", main);