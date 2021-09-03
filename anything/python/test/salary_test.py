import unittest
from unittest.mock import MagicMock
from unittest import mock

import salary

class TestSalary(unittest.TestCase):
    def test_calculation_salary(self):
        s = salary.Salary(year=2017)
        # ここでモックとしての振る舞いを定義する！
        s.bonus_api.bonus_price = MagicMock(return_value=1)

        self.assertEqual(s.calculation_salary(), 101)
        # ちゃんと関数などが呼ばれたかどうかチェック
        s.bonus_api.bonus_price.assert_called()
        s.bonus_api.bonus_price.assert_called_once()
        s.bonus_api.bonus_price.assert_called_with(year=2017)
        self.assertEqual(s.bonus_api.bonus_price.call_count, 1)

    def test_calculation_salary_no_salary(self):
        s = salary.Salary(year=2050)
        # ここでモックとしての振る舞いを定義する！
        s.bonus_api.bonus_price = MagicMock(return_value=0)
        self.assertEqual(s.calculation_salary(), 100)
        s.bonus_api.bonus_price.assert_not_called()

    # モックとして扱うことの宣言
    @mock.patch('salary.ThirdPartyBounusRestApi.bonus_price')
    def test_calculation_salary_patch(self, mock_bonus):
        mock_bonus.return_value = 1

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        s.bonus_api.bonus_price.assert_called()

    def test_calculation_salary_patch_with(self):
        with mock.patch(
            'salary.ThirdPartyBounusRestApi.bonus_price') as mock_bonus:
            mock_bonus.return_value = 1

            s = salary.Salary(year=2017)
            salary_price = s.calculation_salary()

            self.assertEqual(salary_price, 101)
            s.bonus_api.bonus_price.assert_called()

    def setUp(self):
        # 絶対にモックにするものがあるなら、setUp でのパッチが便利！
        self.patcher = mock.patch('salary.ThirdPartyBounusRestApi.bonus_price')
        self.mock_bonus = self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_calculation_salary_patch_with_patcher(self):

        self.mock_bonus.return_value = 1

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        self.mock_bonus.assert_called()

    def test_calculation_salary_patch_with_patch_side_effect(self):
        def f(year):
            return year * 2

        # side effect で、自分の関数を渡せる
        # self.mock_bonus.side_effect = f
        # self.mock_bonus.side_effect = lambda year: 1
        # self.mock_bonus.side_effect = ConnectionRefusedError
        self.mock_bonus.side_effect = [
            1,
            2,
            3,
            ValueError('Bankrupt!!!')]

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()
        self.assertEqual(salary_price, 101)
        s = salary.Salary(year=2018)
        salary_price = s.calculation_salary()
        self.assertEqual(salary_price, 102)
        s = salary.Salary(year=2019)
        salary_price = s.calculation_salary()
        self.assertEqual(salary_price, 103)
        s = salary.Salary(year=200)
        with self.assertRaises(ValueError):
            s.calculation_salary()

    # クラスごと全部モックにする
    # spec true で、全てをモックとして認識してくれる
    @mock.patch('salary.ThirdPartyBounusRestApi', spec=True)
    def test_calculation_salary_patch(self, MockRest):
        mock_rest = MockRest.return_value
        # mock_rest = MockRest()
        mock_rest.bonus_price.return_value = 1

        s = salary.Salary(year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        mock_rest.bonus_price.assert_called()


if __name__ == '__main__':
    # python -m unittest ~ or following
    unittest.main()
