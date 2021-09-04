import collections


d = {}
l = ['a', 'a', 'a', 'b', 'b', 'c']
for word in l:
    if word not in d:
        d[word] = 0
    d[word] += 1
print(d)

d = {}
l = ['a', 'a', 'a', 'b', 'b', 'c']
for word in l:
    d.setdefault(word, 0)
    d[word] += 1
print(d)

d = collections.defaultdict(int)
l = ['a', 'a', 'a', 'b', 'b', 'c']
for word in l:
    d[word] += 1
print(d)

d = collections.defaultdict(set)
s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4),
        ('red', 1), ('blue', 4)]
for k, v in s:
    d[k].add(v)
print(d)


## counter
c = collections.Counter()
l = ['a', 'a', 'a', 'b', 'b', 'c', 'b', 'b', 'c']
for word in l:
    c[word] += 1
print(c)
print(c.most_common(1))
print(c.most_common(2))
print(sum(c.values()))


# 一番多い文字を抽出する
import re
path_to_this_file = './anything/python/tools/collections_count.py'
with open(path_to_this_file, 'r') as f:
    words = re.findall(r'\w+', f.read().lower())
    # print(words)
    print(collections.Counter(words).most_common(20))
