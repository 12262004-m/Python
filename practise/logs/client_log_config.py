import sys
import os
import logging
sys.path.append('../')
from files.variables import LOGGING_LEVEL

CLIENT_FORMAT = logging.Formatter('%(levelname)-10s %(asctime)s %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

STREAM_HAND = logging.StreamHandler(sys.stderr)
STREAM_HAND.setFormatter(CLIENT_FORMAT)
STREAM_HAND.setLevel(logging.ERROR)
LOG_FILE = logging.FileHandler(PATH, encoding='utf8')
LOG_FILE.setFormatter(CLIENT_FORMAT)

LOG = logging.getLogger('client')
LOG.addHandler(STREAM_HAND)
LOG.addHandler(LOG_FILE)
LOG.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOG.critical('Критическая ошибка')
    LOG.error('Ошибка')
    LOG.debug('Отладочная информация')
    LOG.info('Информационное сообщение')