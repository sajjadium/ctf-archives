import hashlib
import html
import os
import secrets

from server import Server

ADMIN_PASSWORD = hashlib.md5(
    f'password-{secrets.token_hex}'.encode()
).hexdigest()

pastes = {}

def add_paste(paste_id, content, admin_only=False):
    pastes[paste_id] = {
        'content': content,
        'admin_only': admin_only,
    }

server = Server()

@server.get('/')
async def root(request):
    del request
    return (200, '''
        <link rel="stylesheet" href="/style.css">
        <div class="container">
            <h1>Pastebin</h1>
            <form action="/paste" method="post">
                <textarea
                    name="content"
                    rows="10"
                    placeholder="Content..."
                ></textarea>
                <input type="submit" value="Create Paste">
            </form>
        </div>
    ''')

@server.post('/paste')
async def paste(request):
    data = await request.post()
    content = data.get('content', '')
    paste_id = id(content)

    add_paste(paste_id, content)

    return (200, f'''
        <link rel="stylesheet" href="/style.css">
        <div class="container">
            <h1>Paste Created</h1>
            <p><a href="/view?id={paste_id}">View Paste</a></p>
        </div>
    ''')

@server.get('/view')
async def view_paste(request):
    id = request.query.get('id')
    paste = pastes.get(int(id))

    if paste is None:
        return (404, 'Paste not found')

    if paste['admin_only']:
        password = request.query.get('password', '')
        if password != ADMIN_PASSWORD:
            return (
                403,
                f'Incorrect parameter &password={ADMIN_PASSWORD[:6]}...',
            )

    return (200, f'''
        <link rel="stylesheet" href="/style.css">
        <div class="container">
            <h1>Paste</h1>
            <pre>{html.escape(paste['content'])}</pre>
        </div>
    ''')

@server.get('/style.css', c_type='text/css')
async def style(request):
    del request
    return (200, '''
        * {
          font-family: system-ui, -apple-system, BlinkMacSystemFont,
            'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
          box-sizing: border-box;
        }

        html,
        body {
          margin: 0;
        }

        .container {
          padding: 2rem;
          width: 90%;
          max-width: 900px;
          margin: auto;
        }

        input:not([type='submit']) {
          width: 100%;
          padding: 8px;
          margin: 8px 0;
        }

        textarea {
          width: 100%;
          padding: 8px;
          margin: 8px 0;
          resize: vertical;
          font-family: monospace;
        }

        input[type='submit'] {
          margin-bottom: 16px;
        }
    ''')

add_paste(0, os.getenv('FLAG', 'missing flag'), admin_only=True)
server.run('0.0.0.0', 3000)
