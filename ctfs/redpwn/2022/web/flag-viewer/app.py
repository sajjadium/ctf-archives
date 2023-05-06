import os
import random

from server import Server

server = Server()

@server.get('/')
async def root(request):
    return (200, '''
        <title>Flag Viewer</title>
        <link rel="stylesheet" href="/style.css" />
        <div class="container">
            <h1>The Flag Viewer</h1>
            <form action="/flag" method="POST">
                <input
                    type="text"
                    name="user"
                    placeholder="Username"
                    pattern="^(?!admin).*$"
                    oninvalid="this.setCustomValidity('Name not allowed!')"
                    oninput="this.setCustomValidity('')"
                />
                <input type="submit" value="Submit" />
            </form>
            <div>%s</div>
        </div>
    ''' % (
        request.query.get('message', '').replace('<', '&lt;'),
    ))


@server.post('/flag')
async def flag(request):
    data = await request.post()
    user = data.get('user', '')

    if user != 'admin':
        return (302, '/?message=Only the "admin" user can see the flag!')

    return (302, f'/?message={os.environ.get("FLAG", "flag missing!")}')

@server.get('/style.css', c_type='text/css')
async def style(request):
    del request
    return (200, '''
        * {
            font-family: 'Helvetica Neue', sans-serif;
            box-sizing: border-box;
        }

        html, body { margin: 0; }

        .container {
            padding: 2rem;
            width: 90%;
            max-width: 900px;
            margin: auto;
        }

        input:not([type="submit"]) {
            width: 100%;
            padding: 8px;
            margin: 8px 0;
        }
    ''')

server.run('0.0.0.0', 3000)
