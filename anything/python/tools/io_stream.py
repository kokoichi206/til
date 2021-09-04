import io
import requests
import zipfile
import tarfile

# with open('/tmp/a.txt', 'w') as f:
#     f.write('test test')

# io は、インメモリストリーム。
# ファイルに書かなくても同様なことができる
# f = io.StringIO()
# f.write('string io test')
# f.seek(0)
# print(f.read())

# f = io.BytesIO()
# f.write(b'string io test')
# f.seek(0)
# print(f.read())


url = ('https://files.pythonhosted.org/packages/46/44'
        '/648b37b1dc8f6e70c05c0f91cc7873b76484a924b8a2d5'
        'aa2e57d6846076/setuptools-36.2.3.zip')
f = io.BytesIO()

r = requests.get(url)
# インメモリに書き込まれているので、ディスクに書き込む必要がない。
f.write(r.content)

with zipfile.ZipFile(f) as z:
    with z.open('setuptools-36.2.3/README.rst') as f:
        print(f.read().decode())
