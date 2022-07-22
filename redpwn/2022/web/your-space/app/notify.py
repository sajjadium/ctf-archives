import json
from io import StringIO
from multiprocessing import Process, Queue
import pycurl

queue = Queue()


def notify_single(url, body):
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(
        pycurl.HTTPHEADER,
        [
            "Accept: application/json",
            "Content-Type: application/json",
        ],
    )
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.TIMEOUT_MS, 1000)

    c.setopt(pycurl.READDATA, StringIO(body))
    c.setopt(pycurl.WRITEFUNCTION, len)
    c.setopt(pycurl.POSTFIELDSIZE, len(body))

    c.perform()


def worker(queue):
    while True:
        url, body = queue.get()
        try:
            notify_single(url, body)
        except:
            pass


def notify(post):
    for sub in post.space.subscriptions:
        url = sub.user.webhook
        body = {
            "space": post.space.name,
            "content": post.content,
            "timestamp": post.timestamp.timestamp(),
        }
        body = json.dumps(body)
        queue.put((url, body))


def start_notifier():
    p = Process(target=worker, args=(queue,))
    p.daemon = True
    p.start()
