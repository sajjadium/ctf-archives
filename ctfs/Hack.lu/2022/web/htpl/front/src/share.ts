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

function main() {
  const hash = location.hash;
  const textarea = document.querySelector<HTMLTextAreaElement>(
    "textarea[name=program]"
  )!;
  const output = document.querySelector<HTMLPreElement>("#output")!
  if (hash) {
    const program = window.atob(hash.slice(1));
    textarea.value = program;
  }

  const form = document.querySelector<HTMLFormElement>("form")!;

  form.addEventListener("submit", async (e: SubmitEvent) => {
    e.preventDefault();
    output.textContent = "An admin is checking your program...";
    const r = await post<{ success: true; result: string } | { success: false }>(
      "/api/submit",
      { program: textarea.value }
    );
    if (r.success){
      output.textContent = r.result;
    } 
  });
}

window.addEventListener("DOMContentLoaded", main);
