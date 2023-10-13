import json
import subprocess
from queue import Queue
from threading import Thread, current_thread

import log
import config

bot_queue = Queue()
POISON_PILL = 'POISON_PILL'
workers = []


def start_worker(i):
    t = Thread(name='worker-{}'.format(i), target=worker_main, args=[i])
    t.start()
    workers.append(t)


def kill_one_worker():
    bot_queue.put(POISON_PILL)


def kill_all_workers():
    for _ in range(len(workers)):
        kill_one_worker()


def add_task(task):
    log.log('[flask]', 'Adding {}'.format(task))
    position = bot_queue.qsize() + 1
    bot_queue.put(task)
    return position


def queue_size():
    return bot_queue.qsize()


def worker_main(i):
    global config, workers
    tag = '[worker-{}]'.format(i)

    log.log(tag, 'started')
    while i < config.config['worker_count']:
        try:
            task = bot_queue.get(block=True, timeout=5)
        except:
            continue

        # abort condition, stop working
        if task == POISON_PILL:
            return
        
        # work on the task
        visit_link(tag, *task)
    
    # remove myself from the worker list
    workers.remove(current_thread())
    log.log(tag, 'stopped')


def visit_link(tag, link, loginInfo={}):
    global config

    log.log(tag, 'Visiting {} {}'.format(link, loginInfo))

    docker_args = [
        'docker', 'run',
        
        # run interactive
        '-i',
        
        # remove container after execution
        '--rm',
        
        # use a specific network
        '--network', config.config['docker_network'],

        # seccomp chrome
        # '--security-opt', 'seccomp=chrome.json',

        # limit run time
        '-e', 'TIMEOUT_SECS={}'.format(config.config['timeout_secs']),

        # the image to run
        config.config['docker_image'],
    ]

    args = docker_args + [
        # the link to visit
        link,

        # the cookies
        json.dumps(loginInfo)
    ]

    log.log(tag, 'Executing: {}'.format(args))
    subprocess.run(args)
