import os
import pytest


@pytest.fixture
def csv_file():
    return 'csv file!!!'

@pytest.fixture
def csv_filer():
    # yield を使うと、閉じる処理なんかまでやってくれる！
    with open('test.csv', 'w+') as c:
        print('before test')
        yield c
        print('after test')

@pytest.fixture
def csv_filer2(tmpdir): # fixture の中でも fixture が使える！
    # yield を使うと、閉じる処理なんかまでやってくれる！
    with open(os.path.join(tmpdir, 'test.csv'), 'w+') as c:
        print('before test')
        yield c
        print('after test')

def pytest_addoption(parser):
    parser.addoption('--os-name', default='linux', help='os name')
