from modules.functions import mult
import pytest
import allure

class TestMult:

    def test_mult_1(self, params_for_mult_test):
        """Тест, использующий фикстуру"""
        a = params_for_mult_test['val1']
        b = params_for_mult_test['val2']
        expect_result = params_for_mult_test['mul']
        result = mult(a, b)
        assert expect_result == result, 'oops'

    @pytest.mark.parametrize(
        ("a", "b"), 
        [(1,2),(3,4),(5,6),(7,8)]
    )
    def test_mult_2(self, a, b):
        """Тест, использующий параметризацию"""
        expect_result = a * b
        result = mult(a, b)
        assert result == expect_result
    
    def test_mult_3(self, fixture_with_params):
        """Тест-функция, использующая фикстуру с параметрами"""
        a, b = fixture_with_params
        expect_result = a * b
        result = mult(a, b)
        assert expect_result == result

    