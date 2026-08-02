import html
import os
import unicodedata
from pathlib import Path, PurePosixPath

from flask import Flask, abort, jsonify, request


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080
MAX_FILE_BYTES = 64 * 1024
BASE_DIR = (Path(__file__).parent / "documents").resolve()

app = Flask(__name__)


def iter_visible_files() -> list[str]:
    visible_files: list[str] = []
    for candidate in sorted(BASE_DIR.rglob("*")):
        if not candidate.is_file():
            continue

        relative_parts = candidate.relative_to(BASE_DIR).parts
        if any(part.startswith(".") for part in relative_parts):
            continue

        visible_files.append(candidate.relative_to(BASE_DIR).as_posix())
    return visible_files


def resolve_document(raw_path: str) -> Path:
    requested_path = raw_path.strip()
    if not requested_path:
        abort(400, "missing path")

    if "\x00" in requested_path:
        abort(400, "invalid path")

    if "\\" in requested_path:
        abort(400, "backslashes are not allowed")

    pure_path = PurePosixPath(requested_path)
    if pure_path.is_absolute():
        abort(400, "absolute paths are not allowed")

    if any(part in {"", ".", ".."} or part.startswith(".") for part in pure_path.parts):
        abort(400, "invalid path segments")

    safe_path = unicodedata.normalize("NFKC", str(pure_path))

    candidate = BASE_DIR / safe_path

    try:
        candidate.relative_to(BASE_DIR)
    except ValueError as exc:
        raise abort(403, "path escapes document root") from exc

    resolved = candidate.resolve(strict=True)
    if not resolved.is_file():
        abort(404, "document not found")

    return candidate


@app.get("/")
def home() -> str:
    items = "\n".join(
        f"<li><code>{html.escape(path)}</code></li>" for path in iter_visible_files()
    )
    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Paper Trail</title>
    <style>
      :root {{
        color-scheme: light;
        font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
        background: #f5f0e8;
        color: #1b1b1b;
      }}
      body {{
        margin: 0;
        min-height: 100vh;
        background: radial-gradient(circle at top, #fff7dc, #efe6d6 60%, #e6dac6);
      }}
      main {{
        width: min(720px, calc(100vw - 2rem));
        margin: 3rem auto;
        padding: 2rem;
        background: rgba(255, 252, 245, 0.88);
        border: 1px solid #ccbda7;
        box-shadow: 0 24px 60px rgba(69, 47, 13, 0.12);
      }}
      h1 {{ margin-top: 0; font-size: 2rem; }}
      code {{ font-family: "IBM Plex Mono", monospace; }}
      ul {{ padding-left: 1.2rem; }}
      .hint {{ color: #60491f; }}
    </style>
  </head>
  <body>
    <main>
      <h1>Paper Trail</h1>
      <p class=\"hint\">Read one document with <code>GET /api/files?path=&lt;relative-path&gt;</code>.</p>
      <p>Available documents:</p>
      <ul>{items}</ul>
    </main>
  </body>
</html>"""


@app.get("/api/files")
def read_file() -> tuple[dict[str, str], int]:
    requested_path = request.args.get("path", "")
    try:
        document_path = resolve_document(requested_path)
    except FileNotFoundError:
        abort(404, "document not found")

    file_size = document_path.stat().st_size
    if file_size > MAX_FILE_BYTES:
        abort(413, "document too large")

    return (
        jsonify(
            {
                "path": document_path.relative_to(BASE_DIR).as_posix(),
                "content": document_path.read_text(encoding="utf-8"),
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", DEFAULT_HOST), port=int(os.getenv("PORT", DEFAULT_PORT)))