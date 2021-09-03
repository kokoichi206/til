"""
REST
"""
import urllib.request
import json


payload = {'key1': 'value1', 'key2': 'value2'}

payload = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    'http://httpbin.org/post', data=payload, method='POST')
with urllib.request.urlopen(req) as f:
    print(f.read().decode('utf-8'))

# url = "http://httpbin.org/get" + '?' + urllib.parse.urlencode(payload)
# print(url)

# with urllib.request.urlopen(url) as f:
#     # print(f.read().decode('utf-8'))
#     r = json.loads(f.read().decode('utf-8'))
#     print(type(r))
#     print(r)


# url = "http://httpbin.org/get"

# with urllib.request.urlopen(url) as f:
#     # print(f.read().decode('utf-8'))
#     r = json.loads(f.read().decode('utf-8'))
#     print(type(r))
#     print(r)
