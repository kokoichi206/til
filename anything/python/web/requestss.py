import requests


# サードパーティー製の、直感的なやつ
payload = {'key1': 'value1', 'key2': 'value2'}

r = requests.get('http://httpbin.org/get', params=payload, timeout=1)

print(r.status_code)
print(r.text)
print(r.json())


r = requests.post('http://httpbin.org/post', data=payload)
print(r.status_code)
print(r.text)
print(r.json())
