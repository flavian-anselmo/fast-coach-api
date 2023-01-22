'''
background, periodic tasks with celery 

'''

'''import celery -> '''
from celery import Celery

''' celery instance > '''
celery_app = Celery(
    'tasks',
    broker = 'amqp://papa:admin@localhost:5672',
    #backend = 'rabbitmq'
)


''' celery task '''
@celery_app.task
def divide(x, y):
    import time
    time.sleep(5)
    res = x / y
    return {'message': f'the answer is {res}'}