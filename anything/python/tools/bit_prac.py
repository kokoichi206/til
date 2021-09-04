print(0 | 0)
print(0 | 1)
print(1 | 0)
print(1 | 1)
print()

print(0 & 0)
print(0 & 1)
print(1 & 0)
print(1 & 1)
print()

print(0 ^ 0)
print(0 ^ 1)
print(1 ^ 0)
print(1 ^ 1)
print()

print(bin(0))
print(bin(~0))
print(bin(~~0))
print(bin(~1))
print()

# 1 * 2 * 2 * 2
# 1 <<< 3
print(bin(1 << 0))
print(bin(1 << 1))
print(bin(1 << 2))
print(bin(1 << 3))
print(bin(1 << 3))
print(bin(1 << 3 >> 2))
print(bin(5))
print(bin(5 >> 1))
print()

# 192.168.1.10 255.255.255.0
print(192 & 255, 168 & 255, 1 & 255, 10 & 0)

# ブロードキャストアドレス
print(192 | 0, 168 | 0, 1 | 0, 10 | 255)

print(192 ^ 0, 168 ^ 0, 1 ^ 0, 10 ^ 255)

print(192 & ~255, 168 & ~255, 1 & ~255, 10 & ~0)
