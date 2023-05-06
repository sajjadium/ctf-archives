import os

from server import Server

server = Server()


@server.get('/')
async def root(request):
    admin = request.cookies.get('admin', '')

    headers = {}
    if admin == '':
        headers['set-cookie'] = 'admin=false'

    if admin == 'true':
        return (200, '''
            <title>Secure Page</title>
            <link rel="stylesheet" href="/style.css" />
            <div class="container">
                <h1>Secure Page</h1>
                %s
            </div>
        ''' % os.environ.get('FLAG', 'flag is missing!'), headers)
    else:
        return (200, '''
            <title>Secure Page</title>
            <link rel="stylesheet" href="/style.css" />
            <div class="container">
                <h1>Secure Page</h1>
                Sorry, you must be the admin to view this content!
            </div>
        ''', headers)


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
