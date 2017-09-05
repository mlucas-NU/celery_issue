import logging
from worker import add, gcv_task

# Simple task: addition
logging.info('About to enqueue ADD')
async_process = add.delay(3, 4)
logging.info('Waiting for ADD response...')
result = async_process.get()
logging.info('ADD result: {}'.format(result))

# Google Cloud Vision
logging.info('About to enqueue GCV task')
async_process = gcv_task.delay()
logging.info('Waiting for GCV response...')
result = async_process.get()
logging.info('OCR response: {}'.format(result))
