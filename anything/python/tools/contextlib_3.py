import contextlib
import os


try:
    os.remove('somefile.tmp')
except FileNotFoundError:
    pass

# エラー抑圧するのなら、このように書くこともできる
with contextlib.suppress(FileNotFoundError):
    os.remove('somefile.tmp')
    os.remove('somefile2.tmp')
