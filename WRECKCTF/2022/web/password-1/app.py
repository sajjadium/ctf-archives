import os
from server import Server

FLAG = os.environ.get('FLAG', 'flag missing!')

server = Server()


@server.get('/')
async def root(request):
    del request
    return (200, '''
        <link rel="stylesheet" href="/style.css" />
        <div class="container">
            <form class="content">
                <input type="text" placeholder="Password..."/>
                <input type="submit" value="Login" />
            </form>
        </div>
        <script>
            const sha256 = async (message) => {
              const data = (new TextEncoder()).encode(message);
              const hashed = await crypto.subtle.digest('SHA-256', data);
              return Array.from(new Uint8Array(hashed))
                .map((b) => b.toString(16).padStart(2, '0'))
                .join('')
            }

            (() => {
              const form = document.querySelector('form');
              form.addEventListener('submit', async (event) => {
                event.preventDefault();
                const input = document.querySelector('input[type="text"]');
                const hash = (
                  '8c59346d674a352c' +
                  'aa36c0cb808ec0dd' +
                  '28ba42144f760c12' +
                  '564663b610c9ce2d'
                );
                if (await sha256(input.value) === hash) {
                  const flag = await (await fetch('/api/output')).text();
                  document.querySelector('.content').textContent = flag;
                } else {
                  input.removeAttribute('style');
                  input.offsetWidth;
                  input.style.animation = 'shake 0.25s';
                }
              });
            })();
        </script>
    ''')


@server.get('/style.css', c_type='text/css')
async def style(request):
    del request
    return (200, '''
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            font-family: sans-serif;
        }

        body {
            background-color: rebeccapurple;
        }

        .incorrect {
            animation: shake 0.25s;
        }

        .content {
            transform: scale(4);
            background-color: white;
            padding: 2rem;
            border-radius: 0.5rem;
            max-width: 18vw;
        }

        .container {
            height: 100%;
            display: grid;
            place-items: center;
        }

        @keyframes shake {
            0% { transform: rotate(0deg); }
            25% { transform: rotate(5deg); }
            50% { transform: rotate(0eg); }
            75% { transform: rotate(-5deg); }
            100% { transform: rotate(0deg); }
        }
    ''')


@server.get('/api/output', c_type='text/plain')
async def flag(request):
    del request
    return (200, FLAG)


server.run('0.0.0.0', 3000)
