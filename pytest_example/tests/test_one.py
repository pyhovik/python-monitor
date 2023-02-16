from modules.functions import sum
import random
import pytest
import allure

@pytest.mark.usefixtures('session_fixture')
class TestSum:

    #@pytest.mark.skipif(random.randint(-2, 2) == 0, reason="random skip, hehe")
    def test_positive_int_sum(self):
        """Тест-функция, не использующая фикстуры"""

        if random.randint(-3, 3) == 0:
            pytest.skip('oops')
        
        if random.randint(-3, 3) == 1:
            pytest.xfail('meow')
        
        with allure.step("Присваиваем рандомные переменные: a, b"):
            a = random.randint(0, 100)
            b = random.randint(0, 100)
            expect_result = a + b
            assert expect_result
        
        with allure.step("Вызываем функцию sum(a, b)"):
            result = sum(a, b)
            assert result

        with allure.step("Проверяем результат"):
            assert expect_result == result

    @allure.description("Проверяем сумму отрицательных чисел")
    def test_negative_int_sum(self, params_for_sum_test):
        """Тест-функция, использующая фикстуру (scope=function)"""
        a = params_for_sum_test[0]
        b = params_for_sum_test[1]
        expect_result = a + b
        result = sum(a, b)
        assert result == expect_result
    
    @pytest.mark.parametrize(
        ("a", "b"), 
        [(-1.5, 2.4), (3.0, 4.1),(5, 6.0)]
    )
    def test_float_sum(self, a, b):
        """Параметризованный тест"""
        expect_result = a + b
        result = sum(a, b)
        assert type(result) == float
        assert expect_result == result