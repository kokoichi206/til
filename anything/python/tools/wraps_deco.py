import functools


def d(f):
    @functools.wraps(f)
    def w():
        """Wrapper docstring"""
        print('decorator')
        return f()
    return w

@d
def example():
    """Example docstring"""
    print('example')

help(example)
print(example.__doc__)

# example()



# def d(f):
#     def w():
#         print('decorator')
#         return f()
#     return w

# @d
# def example():
#     print('example')

# example()
