Supply chain attacks? Code leaks? Never heard of those.

Here at Example.com, we store our entire production environment on GitHub! Our code monkeys are so talented that they would never do anything stupid that would get accounts compromised or anything like that.

# Login Extension for Flask

The simplest way to add login to flask!

## How it works

First, install it from [PyPI](https://pypi.org/project/flask_simplelogin/):

```console
$ pip install flask_simplelogin
```

Then, use it in your app:

```python
from flask import Flask
from example.flask_simplelogin import SimpleLogin

app = Flask(__name__)
SimpleLogin(app)
```

## **That's it!**

Now you have `/login` and `/logout` routes in your application.

The username defaults to `admin` and the password defaults to `secret` — yeah that's not clever, check the [docs](https://flask-simple-login.readthedocs.io/en/latest/?badge=latest) to see how to configure it properly!

Check the [documentation](https://flask-simple-login.readthedocs.io/en/latest/?badge=latest) for more details!

# Usage

Run with:

```bash
python app.py
```

The `manage.py`

A complete application using Flask factories, click commands and storing
passwords encrypted in a json file `users.json` which you can easily take
as example to replace with your own database manager.

> NOTE: this example is not meant for production use as writing in a json file
> is suitable only for single access. Go with MongoDb, TinyDB or other SGDB.

Run with:

```bash
python manage.py
```

Create new user:

```bash
python manage.py adduser
```

Run the server

```bash
python manage.py runserver
```
