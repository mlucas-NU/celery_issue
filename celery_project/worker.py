import logging
import os

from celery import Celery
from celery.utils.log import get_logger
from google.cloud import vision
from google.cloud.vision import types

cloud_logger = logging.getLogger('cloudLogger')
cloud_logger.setLevel(logging.DEBUG)

celery_app = Celery('tasks', backend='rpc', broker='172.25.1.0')
celery_app.log.setup(loglevel=logging.INFO)
logger = get_logger(__name__)


@celery_app.task()
def add(x, y):
    return x + y


@celery_app.task()
def gcv_task():
    gcv_label_cat()


def gcv_label_cat():
    client = vision.ImageAnnotatorClient()

    cat_path = os.path.join(os.path.dirname(__file__), 'cat.jpg')
    with open(cat_path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    logger.info('Connecting to GCV...')
    response = client.label_detection(image=image)
    labels = response.label_annotations
    logger.info('Labels:')

    for label in labels:
        logger.info(label.description)


if __name__ == '__main__':
    logger.info('Executing locally')
    gcv_label_cat()
    logger.info('Finished with local')
    celery_app.start()
