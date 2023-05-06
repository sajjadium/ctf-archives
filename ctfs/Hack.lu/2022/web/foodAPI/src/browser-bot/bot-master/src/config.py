import json
from time import sleep
from threading import Thread

from log import log
from worker import workers, start_worker, kill_one_worker

config = {}
old_config = {}
config_load = None
config_loader = None
running = True


def init_config(config_file):
    global config_loader
    load_config(config_file)
    config_loader = Thread(name='config-loader', target=config_loader_main, args=[config_file])
    config_loader.start()


def stop_config_loader():
    global running
    running = False
    config_loader.join()


def config_loader_main(config_file):
    global running
    while running:
        load_config(config_file)
        sleep(1)


def load_config(config_file):
    global config, old_config, workers

    # parse the config file
    with open(config_file, 'r') as f:
        new_config = json.loads(f.read())

    any_changes = False
    for key in set(list(old_config.keys()) + list(new_config.keys())):
        old_value = old_config[key] if key in old_config else None
        new_value = new_config[key] if key in new_config else None
        if old_value != new_value:
            log('[config]', "{} changed from '{}' to '{}'".format(key, old_value, new_value))
            any_changes = True

    if not any_changes:
        return
    else:
        old_config = new_config.copy()
        config = new_config

    # recaptcha keys
    config['use_recaptcha'] = config.get('use_recaptcha', False)
    if config.get('use_recaptcha', False) is True:
        if config['recaptcha_public_key'] is None or config.get('recaptcha_secret_key', None) is None:
            raise Exception('recaptcha_public_key and recaptcha_secret_key must be defined in config')

    # link pattern
    if config.get('link_pattern', None) is None:
        config['link_pattern'] = '^https?://'

    # default cookie
    if config.get('cookies', None) is None:
        config['cookies'] = []

    # default timeout
    if config.get('timeout_secs', None) is None:
        config['timeout_secs'] = 30

    # worker count
    current_worker_count = len(workers)
    if config.get('worker_count', None) is None:
       config['worker_count'] = 1 
    if config['worker_count'] > current_worker_count:
        # spawn more workers
        for i in range(current_worker_count, config['worker_count']):
            start_worker(i)
    elif config['worker_count'] < current_worker_count:
        # kill some workers
        for i in range(config['worker_count'], current_worker_count, -1):
            kill_one_worker()

    # docker stuff
    if config.get('docker_image', None) is None:
        config['docker_image'] = 'chrome-bot'

