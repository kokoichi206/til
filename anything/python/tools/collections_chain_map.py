import collections


a = {'a': 'a', 'c': 'c', 'num': 0}
b = {'b': 'b', 'c': 'cc'}
c = {'b': 'bbb', 'c': 'ccc'}

class DeepChainMap(collections.ChainMap):
    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                if type(mapping[key]) is int and mapping[key] < value:
                    mapping[key] = value
                return
        self.maps[0][key] = value

m = DeepChainMap(a, b, c)
m['new_num'] = -1
print(m['new_num'])
m['new_num'] = 1
print(m['new_num'])

m['num'] = -1
print(m['num'])
m['num'] = 1
print(m['num'])

# print(a)
# a.update(b)
# print(a)
# a.update(c)
# print(a)

# # すきたなタイミングで dict を操作できる
# # いつ使いそうかな〜？？
# m = collections.ChainMap(a, b, c)
# print(m)
# print(m.maps)   # これはリスト！！
# print(m['c'])
# m.maps.reverse()
# print(m['c'])
# m.maps.insert(0, {'c': 'CCCCC'})
# print(m['c'])
# del m.maps[0]
# print(m.maps)
# print(m['c'])
# m['b'] = 'BBBBB'
# print(m.maps)
