import subprocess

SIZE = 100_0000

print("before memory allocation")
subprocess.run("free")

array = [0] * SIZE

print("after memory allocation")
subprocess.run("free")
