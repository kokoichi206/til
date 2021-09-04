def s_hello():
    yield 'hello 1'
    yield 'hello 2'
    yield 'hello 3'
    return 'done'

# generator ベースコルーチン
def g_hello():
    while True:
        # r = yield 'hello'
        r = yield from s_hello()
        yield r

g = g_hello()
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))

# print(next(g))
# print(g.send('plus'))
# print(next(g))
# print(g.send('nancy'))
# print(next(g))
# print(g.send('hoge'))
