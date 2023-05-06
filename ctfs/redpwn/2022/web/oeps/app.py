import os
import random
import sqlite3

from server import Server

# database stuff
connection = sqlite3.connect(':memory:')

def init():
    connection.execute('''
        create table approved (
            id integer primary key autoincrement,
            sentence text
        );
    ''')

    connection.execute('''
        create table pending (
            id integer primary key autoincrement,
            user text,
            sentence text
        );
    ''')

    connection.execute('''
        create table users (
            token text
        );
    ''')

    connection.execute('''
        create table flags (
            flag text
        );
    ''')

    initial = [
        'rats live on no evil star',
        'kayak',
        'mr owl ate my metal worm',
        'do geese see god',
        '313',
        'a man a plan a canal panama',
        'doc note i dissent a fast never prevents a fatness i diet on cod',
        'live on time emit no evil',
    ]

    for palindrome in initial:
        connection.execute('''
            insert into approved (sentence) values ('%s');
        ''' % palindrome)

    connection.execute('''
        insert into flags (flag) values ('%s');
    ''' % os.environ.get('FLAG', 'flag is missing!'))
init()


# handle requests
ALLOWED_CHARACTERS = set(
    'abcdefghijklmnopqrstuvwxyz' +
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
    '0123456789 '
)

server = Server()

@server.get('/')
async def root(request):
    token = request.cookies.get('token', '')

    requires_cookie = (
        any(c not in ALLOWED_CHARACTERS for c in token) or
        len(connection.execute('''
            select * from users where token = '%s';
        ''' % token).fetchall()) != 1
    )

    headers = {}
    if requires_cookie:
        token = ''.join(random.choice('0123456789abcdef') for _ in range(32))
        headers['set-cookie'] = f'token={token}'
        connection.execute('''
            insert into users (token) values ('%s');
        ''' % token)

    pending = connection.execute('''
        select sentence from pending where user = '%s';
    ''' % token).fetchall()

    return (200, '''
        <title>OEPS</title>
        <link rel="stylesheet" href="/style.css" />
        <div class="container">
            <h1>The On-Line Encyclopedia of Palidromic Sentences</h1>
            Enter a word or phrase:
            <form action="/search" method="GET">
                <input type="text" name="search" placeholder="on" />
                <input type="submit" value="Search" />
            </form>
            <h2>Submit Sentence:</h2>
            New palindrome:
            <form action="/submit" method="POST">
                <input type="text" name="submission" />
                <input type="submit" value="Submit" />
            </form>
            <div style="color: red">%s</div>
            <h2>Pending submissions:</h2>
            <ul>%s</ul>
        </div>
    ''' % (
        request.query.get('error', '').replace('<', '&lt;'),
        ''.join(f'<li>{palindrome}</li>' for (palindrome,) in pending),
    ), headers)

@server.get('/search')
async def search(request):
    if 'error' in request.query:
        return (200, '''
            <title>OEPS</title>
            <link rel="stylesheet" href="/style.css" />
            <div class="container">
                <h1>The On-Line Encyclopedia of Palidromic Sentences</h1>
                Enter a word or phrase:
                <form action="/search" method="GET">
                    <input type="text" name="search" placeholder="on" />
                    <input type="submit" value="Search" />
                </form>
                <div style="color: red">%s</div>
                <hr noshade />
            </div>
        ''' % request.query.get('error', '').replace('<', '&lt;'))
    else:
        search = request.query.get('search', '')

        if search == '':
            return (302, '/search?error=Search cannot be empty!')

        if any(c not in ALLOWED_CHARACTERS for c in search):
            return (302, '/search?error=Search must be alphanumeric!')

        result = connection.execute('''
            select sentence from approved where sentence like '%%%s%%';
        ''' % search).fetchall()
        count = len(result)

        return (200, '''
            <title>OEPS</title>
            <link rel="stylesheet" href="/style.css" />
            <div class="container">
                <h1>The On-Line Encyclopedia of Palidromic Sentences</h1>
                Enter a word or phrase:
                <form action="/search" method="GET">
                    <input type="text" name="search" placeholder="on" />
                    <input type="submit" value="Search" />
                </form>
                <hr noshade />
                <h2>%s</h2>
                <ul>%s</ul>
            </div>
        ''' % (
            'No results.' if count == 0 else f'Results ({count}):',
            ''.join(f'<li>{palindrome}</li>' for (palindrome,) in result),
        ))

@server.post('/submit')
async def submit(request):
    token = request.cookies.get('token', '')
    logged_in = (
        all(c in ALLOWED_CHARACTERS for c in token) and
        len(connection.execute('''
            select * from users where token = '%s';
        ''' % token).fetchall()) == 1
    )

    if not logged_in:
        return (302, '/?error=Authentication error.')

    data = await request.post()
    submission = data.get('submission', '')
    if submission == '':
        return (302, '/?error=Submission cannot be empty.')

    stripped = submission.replace(' ', '')
    if stripped != stripped[::-1]:
        return (302, '/?error=Submission must be a palindrome.')

    connection.execute('''
        insert into pending (user, sentence) values ('%s', '%s');
    ''' % (
        token,
        submission
    ))

    return (302, '/')

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
connection.close()
