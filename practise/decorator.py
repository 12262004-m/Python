import sys
import logging
import inspect
import logs.server_log_config
import logs.client_log_config

def log(func):
    def saver(*args, **kwargs):
        logger_name = 'server' if 'server.py' in sys.argv[0] else 'client'
        LOGGER = logging.getLogger(logger_name)
        f = func(*args, **kwargs)
        LOGGER.debug(f"Вызвана функция {func.__name__} с параметрами {args}, {kwargs} была вызвана из функции {inspect.stack()[1][3]}")
        return f
    return saver
