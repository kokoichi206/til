import logging
import sys


# x = input('Enter: ')
# print(x)

# for line in sys.stdin:
#     print(line)

# print('hello')
# # stdout のストリームに直接書き込む
# sys.stdout.write('hello')

# logging.error('Error')
# sys.stderr.write('Error!')

import contextlib
 
with open('stdout.log', 'w') as f:
    with contextlib.redirect_stdout(f):
        print('hello')
        help(sys.stdout)
