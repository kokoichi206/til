import contextlib

# def tag(name):
#     def _tag(f):
#         def _wrapper(content):
#             print('<{}>'.format(name))
#             r = f(content)
#             print('</{}>'.format(name))
#             return r
#         return _wrapper
#     return _tag

# # f = tag(f) -> f() でも同じ結果を得る
# # @tag('h2')
# def f(content):
#     print(content)

# # f = tag(f)
# f = tag('h1')(f)

# f('hoge')


@contextlib.contextmanager
def tag(name):
    print('<{}>'.format(name))
    yield
    print('</{}>'.format(name))

# with ステートメントにも使える！
with tag('h2'):
    print('test')

def g():
    print('test 0')
    with tag('h2'):
        print('test')
        with tag('h5'):
            print('test2')
g()

# @tag('h2')
# def f(content):
#     print(content)

# f('test')
