import logging


# see
# https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
#
# formatter = '%(levelname)s:%(message)s'
# formatter = '%(asctime)s:%(message)s'
# logging.basicConfig(level=logging.INFO, format=formatter)
# logging.basicConfig(filename='test.logging', level=logging.INFO)

# logging.critical('critical')
# logging.error('error')
# logging.warning('warning')
# logging.info('info')
# logging.debug('debug')


# logging.info('info %s %s' % ('test', 'test2'))
# logging.info('info %s %s', 'test', 'test2')


logging.basicConfig(level=logging.INFO)

logging.info('info')

# 複数ファイルある時は、このようにして、どのファイルから呼ばれたかを記述しておく！
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.debug('debug')


import logtest

logtest.do_something()

