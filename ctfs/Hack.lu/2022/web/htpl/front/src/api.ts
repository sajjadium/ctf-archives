/*
 * The api module provides a simple interface to the backend.
 * This is not part of the challenge.
 */

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

async function get<T>(path: string): Promise<T> {
  const r = await fetch(path);
  return (await r.json()) as T;
}

export async function save(program: string) {
  const { id } = await post<{ id: string }>("/api/save", { program });
  return id;
}

export async function load(id: string) {
  const { program } = await get<{ program: string }>(`/api/load/${id}`);
  return program;
}
