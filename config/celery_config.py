import os
import logging
from celery import Celery, Task
from kombu import Queue, Exchange


class CustomTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if isinstance(exc, ConnectionError):
            logging.error('A connection error has occured and handled by me')
        else:
            print(f'An unexpected exception has occured :\n {exc}')
        return super().on_failure(exc, task_id, args, kwargs, einfo)
    

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
]
app.conf.update({
    'task_queues': [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
    ],
    
    'task_default_priority': 5,
    'task_acks_late': True, 
    'worker_prefetch_multiplier': 1,
    'worker_concurrency': 1,
})

app.Task = CustomTask
app.autodiscover_tasks()
