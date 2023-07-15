<?php
define('API_BASE_URL', getenv('API_BASE_URL') ?: 'http://example.com');
define('API_BASE_URL_FOR_ADMIN', getenv('API_BASE_URL_FOR_ADMIN') ?: 'http://example.com');

function urlsafe_base64_encode($str) {
    $str = base64_encode($str);
    $str = str_replace(['+', '/', '='], ['-', '_', ''], $str);
    return $str;
}

$nonce = urlsafe_base64_encode(random_bytes(16));
header("Content-Security-Policy: default-src 'self'; style-src https://fonts.googleapis.com 'nonce-$nonce'; script-src 'nonce-$nonce'; connect-src " . API_BASE_URL . " " . API_BASE_URL_FOR_ADMIN . "; font-src https://fonts.gstatic.com");
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plain Blog - Frontend Example</title>
    <link href="/style.css" rel="stylesheet" nonce="<?= $nonce ?>">
</head>
<body>
    <h1>Plain Blog - Frontend Example</h1>
    <div id="content">
        Loading...
    </div>

    <template id="index">
        <h2>What is this?</h2>
        <p>Welcome to Plain Blog! This is an example of frontend code for <code><?= API_BASE_URL ?></code>.</p>
        <p>You can add your post from the form below or view a post like <a href="#page=post&id=41071402-ea46-414b-899a-aaf4b2fc4b3b">this link</a>.</p>
        <p>Also, you can view multiple posts at one time like <a href="#page=post&id=41071402-ea46-414b-899a-aaf4b2fc4b3b,a7a74a78-3a82-4c77-a042-f997398af586,1252b5db-7d35-4563-8e1e-4658a8c90daa">this link</a>.</p>

        <h2>Add post</h2>
        <label>
            Title: <input type="text"><br>
        </label>
        <label>
            Content: <textarea cols="30" rows="10"></textarea><br>
        </label>
        <button>Submit</button>
    </template>

    <template id="post">
        <h2>Title</h2>
        <pre>Content</pre>
        <button class="like">👍 0</button>
        <a href="/report.php">appeal to admin to add 1,000 likes</a>
    </template>

    <script nonce="<?= $nonce ?>">
    (async () => {
        let isAdmin = false;

        function request(method, path, body=null) {
            const options = {
                method,
                mode: 'cors'
            };

            if (body != null) {
                options.body = body;
            }

            const baseUrl = isAdmin ? '<?= API_BASE_URL_FOR_ADMIN ?>' : '<?= API_BASE_URL ?>';
            return fetch(`${baseUrl}${path}`, options);
        }

        async function addPost(title, content) {
            const formData = new FormData();
            formData.append('title', title);
            formData.append('content', content);

            const res = await (await request('POST', '/api/post', formData)).json();
            if (!('post' in res)) {
                // ToDo: implement error handling
                return;
            }

            const post = res.post;
            location.assign(`#page=post&id=${post.id}`);
        }

        async function addLike(id, likes) {
            const formData = new FormData();
            formData.append('likes', likes);
            return await (await request('POST', `/api/post/${id}/like`, formData)).json();
        }

        const content = document.getElementById('content');
        const templates = {
            index: document.getElementById('index').content,
            post: document.getElementById('post').content,
        };

        async function renderPost(id, data, likes) {
            const post = templates.post.cloneNode(true);
            const title = post.querySelector('h2');
            title.textContent = data.title;
            const contents = post.querySelector('pre');
            contents.textContent = data.content;

            const button = post.querySelector('.like');
            button.textContent = `👍 ${data.like}`;
            button.addEventListener('click', async () => {
                button.disabled = true;

                const res = await addLike(id, likes);
                button.disabled = false;
                if (!('post' in res)) {
                    // ToDo: implement error handling
                    return;
                }

                button.textContent = `👍 ${res.post.like}`;
            }, false);

            return post;
        }

        async function renderPage() {
            const params = new URLSearchParams(location.hash.slice(1));
            const page = params.get('page') || 'index';
            isAdmin = !!params.get('admin');

            if (page === 'index') {
                const index = templates.index.cloneNode(true);

                const title = index.querySelector('input');
                const contents = index.querySelector('textarea');
                index.querySelector('button').addEventListener('click', () => {
                    addPost(title.value, contents.value);
                }, false);

                content.innerHTML = '';
                content.appendChild(index);
            }

            if (page === 'post' && params.has('id')) {
                const ids = params.get('id').split(',');

                const types = {
                    title: 'string', content: 'string', like: 'number'
                };
                let posts = {}, data, post;
                for (const id of ids) {
                    try {
                        const res = await (await request('GET', `/api/post/${id}`)).json();
                        // ToDo: implement error handling
                        if (res.post) {
                            data = res.post;
                        }

                        // to allow duplicate id but show only once
                        if (!(id in posts)) {
                            posts[id] = {};
                        }
                        post = posts[id];

                        // type check
                        for ([key, value] of Object.entries(data)) {
                            // we don't care the types of properties other than title, content, and like
                            // because we don't use them
                            if (key in types && typeof value !== types[key]) {
                                continue;
                            }

                            post[key] = value;
                        }
                    } catch {}
                }

                content.innerHTML = '';
                for (const [id, post] of Object.entries(posts)) {
                    content.appendChild(await renderPost(id, post, isAdmin ? 1000 : 1));
                }
            }
        }

        renderPage();
        window.addEventListener('hashchange', renderPage);
    })();
    </script>
</body>
</html>