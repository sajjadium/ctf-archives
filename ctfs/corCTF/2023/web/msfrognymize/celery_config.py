from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

celery_app.conf.update(
    result_expires=3600,
    beat_schedule={
        # This is the periodic task to clear the uploads/ folder every 5 minutes
        'clear-uploads-folder': {
            'task': 'tasks.clear_uploads_folder',
            'schedule': crontab(minute='*/5'),
        },
    },
)