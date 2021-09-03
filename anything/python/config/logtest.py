import logging


# サブファイルでは logger を使う
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# このファイルだけ、ログをファイルに出力した時など
h = logging.FileHandler('logtest.log')
logger.addHandler(h)

def do_something():
    logging.info('from logtest info')
    logger.info('from logtest')
    logger.debug('from logtest debug')
