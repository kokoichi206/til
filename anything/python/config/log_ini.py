import logging.config

# dictConfig の方がよくみる形かも〜
logging.config.fileConfig('./anything/python/logging.ini')
logger = logging.getLogger(__name__)
logger = logging.getLogger('simpleExample')

logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
