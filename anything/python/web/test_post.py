import requests


r = requests.get(
    'http://127.0.0.1:5000/employee/hoge'
)
print(r.text)

r = requests.post(
    'http://127.0.0.1:5000/employee', data={'name': 'hoge'}
)
print(r.text)

r = requests.update(
    'http://127.0.0.1:5000/employee', data={
        'name': 'hoge',
        'name': 'fuga'
    }
)
print(r.text)

r = requests.delete(
    'http://127.0.0.1:5000/employee', data={
        'name': 'fuga',
    }
)
print(r.text)
