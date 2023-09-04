import os

STORAGE_PATH='/storage'

ALLOWED_FILE_TYPES = ['.jpeg', '.jpg', '.svg', '.png', '.gif']
ALLOWED_MIME_TYPES = [
    'image/jpeg',
    'image/jpg',
    'image/svg+xml',
    'image/png',
    'image/gif'
]

MONGODB_CONFIG = {
    'host': 'mongodb',
    'port': 27017,
    'username': 'monkeuser',
    'password': 'gonnawhackmykeyboardasi)!@sdjSJED121',
    'database': 'monkeyfsdb',
    'collection': 'files'
}

FLAG = os.environ.get('FLAG', 'FAKE{monk3s_get_the_flag_on_the_challenge_server}')

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'monkeadmin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password123')