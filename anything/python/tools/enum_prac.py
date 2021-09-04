import enum


# permission
class Perm(enum.IntFlag):
    R = 4
    W = 2
    X = 1

print(Perm.R | Perm.W)
print(repr(Perm.R | Perm.W))
print(repr(Perm.R | Perm.W | Perm.X))
RWX = Perm.R | Perm.W | Perm.X
print(Perm.W in RWX)




class Status(enum.Enum):
    ACTIVE = 1
    RENAME_ACTIVE = 1
    INACTIVE = 2
    RUNNING = 3

print(Status.ACTIVE)
print(Status.RENAME_ACTIVE) # CAUTION
# print(Status.STOPPING) # ERROR
print(Status.ACTIVE.name)
print(Status.ACTIVE.value)

for s in Status:
    print(s)
    print(type(s))

# メモリの関係上、String じゃなくて、INT で管理すること多い
db = {
    # 'stac1': 'active',
    # 'stac2': 'inactive',
    'stack1': 1,
    'stack2': 2,
}

if Status(db['stack1']) == Status.ACTIVE:
    print('shutdown')
elif Status(db['stack1']) == Status.INACTIVE:
    print('terminate')

# 出力されない
if db['stack1'] == Status.ACTIVE:
    print('shutdown')
elif db['stack1'] == Status.INACTIVE:
    print('terminate')

print(Status.ACTIVE == 1)
print(Status.ACTIVE == Status(1))

@enum.unique
class Status_hoge(enum.IntEnum):
    ACTIVE = 1
    INACTIVE = 2
    RUNNING = 3

print(Status.ACTIVE == 1)

if db['stack1'] == Status_hoge.ACTIVE:
    print('shutdown hoge')
elif db['stack1'] == Status_hoge.INACTIVE:
    print('terminate hoge')
