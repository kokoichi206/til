import pytest
import os

import calculation

# Usage:
#   pytest pytest_prac.py -s
#   pytest pytest_prac.py --os-name=mac -s
#
# -s: プリント表示する
# conftest.py とかを使う！

# def test_add_num_and_double():
#     cal = calculation.Cal()
#     assert cal.add_num_and_double(1, 1) == 4

class TestCal(object):
    
    @classmethod
    def setup_class(cls):
        print('start')
        cls.cal = calculation.Cal()
        cls.test_dir = '/tmp/test_dir'
        cls.test_file_name = 'test.txt'

    def test_save_no_dir(self):
        self.cal.save(self.test_dir, self.test_file_name)
        test_file_path = os.path.join(self.test_dir, self.test_file_name)
        assert os.path.exists(test_file_path) is True

    @classmethod
    def teadown_class(cls):
        print('end')
        import shutil
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
        del cls.cal
    
    def setup_method(self, method):
        print('method={}'.format(method.__name__))
        # self.cal = calculation.Cal()

    def teardown_method(self):
        print('clean up')
        # del self.cal

    def test_save(self, tmpdir):
        print(tmpdir)   # fixture が勝手にファイルを作ってくれる
        self.cal.save(tmpdir, self.test_file_name)
        test_file_path = os.path.join(tmpdir, self.test_file_name)
        assert os.path.exists(test_file_path) is True

    def test_add_num_and_double(self, request):
        os_name = request.config.getoption('--os-name')
        print(os_name)
        # os_name = 'mac'
        if os_name == 'mac':
            print('ls')
        elif os_name == 'windows':
            print('dir')
        assert self.cal.add_num_and_double(1, 1) == 4

    # @pytest.mark.skip(reason='skip')
    def test_add_num_and_double_raise(self, csv_filer):
        print(csv_filer)
        with pytest.raises(ValueError):
            self.cal.add_num_and_double('1', '1')
