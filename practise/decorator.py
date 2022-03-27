import sys
import logging
import inspect

if sys.argv[0].find("clinnt.py") == -1:
    LOG = logging.getLogger('server')
else:
    LOG = logging.getLogger('client')

def log(func):
    def saver(*args, **kwargs):
        f = func(*args, **kwargs)
        LOG.debug(f"Вызвана функция {func.__name__} с параметрами {args}, {kwargs} была вызвана из функции {inspect.stack()[1][3]}")
        return f
    return saver()
