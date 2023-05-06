import "./style/main.scss";
import { createEditor } from "./editor";

async function post<T>(path: string, body: any): Promise<T> {
  const r = await fetch(path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return (await r.json()) as T;
}

function save(code: string) {
  localStorage.setItem("code", code);
}

function load() {
  return localStorage.getItem("code") || "\n\nclass room: ...";
}

async function main() {
  const runBtn = document.getElementById("run") as HTMLButtonElement;
  const container = document.getElementById("editor")!;
  const outputEl = document.getElementById("output")!;

  async function run() {
    outputEl.innerText = "Running...";
    const { output } = await post<{ output: string }>("/api/submit", { code: load() });
    outputEl.innerText = `Output:\n\n${output}`;
  }

  const code = load();
  save(code);

  const { onChange, onRun } = await createEditor(container, code);

  onChange((code) => {
    save(code);
  });

  onRun(run);
  runBtn.addEventListener("click", run);
}
window.addEventListener("DOMContentLoaded", main);
