import contextlib


# @contextlib.contextmanager
# def tag(name):
#     print('<{}>'.format(name))
#     yield
#     print('</{}>'.format(name))

class tag(contextlib.ContextDecorator):
    def __init__(self, name):
        self.name = name
        self.start_tag = '<{}>'.format(name)
        self.end_tag = '</{}>'.format(name)

    def __enter__(self):
        print(self.start_tag)

    def __exit__(self, exec_type, exc_val, exc_tb):
        print(self.end_tag)

# with ステートメントにも使える！
with tag('h2'):
    print('test')

