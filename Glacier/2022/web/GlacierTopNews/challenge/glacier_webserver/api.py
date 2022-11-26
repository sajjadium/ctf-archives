import multiprocessing
import os
import platform
from urllib import urlopen

import psutil
from flask import request
from glacier_webserver.config import app
from glacier_webserver.utils import Filter
from glacier_webserver.utils import require_jwt


def get_system_info():
    _, _, load15 = psutil.getloadavg()
    cpu_usage = (load15/multiprocessing.cpu_count()) * 100

    env_var = {
      key: os.environ[key]
      for key in os.environ
      if "PORT" not in key and "HOST" not in key and "KEY" not in key
    }

    return {
        'environment': env_var,
        'machine': platform.machine(),
        'version': platform.version(),
        'platform': platform.platform(),
        'system': platform.system(),
        'cpu_usage': cpu_usage,
        'ram_usage': psutil.virtual_memory().percent,
    }


@app.route('/api/system_info', methods=['POST'])
@require_jwt
def get_system_information():
    return get_system_info(), 200, {'Content-Type': 'application/json'}


@app.route('/api/get_resource', methods=['POST'])
def get_resource():
    url = request.json['url']

    if(Filter.isBadUrl(url)):
        return 'Illegal Url Scheme provided', 500

    content = urlopen(url)
    return content.read(), 200
