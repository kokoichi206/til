import json


j = {
    "employee":
        [
            {"id": 111, "name": "Mike"},
            {"id": 222, "name": "Nancy"}
        ]
}

print(j)
print("##########")
print(json.dumps(j))

# Python 内の変数の時は、"s" がつく
a = json.dumps(j)
print(json.loads(a))

with open('test.json', 'w') as f:
    json.dump(j, f)

with open('test.json', 'r') as f:
    print(json.load(f))

