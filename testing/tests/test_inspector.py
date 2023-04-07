"""
Тест-набор для тестирования функций модуля "inspector".
"""
import allure
from app.modules.inspector import Inspector

inspector = Inspector()


class TestInspector:
    
    @allure.title("Проверка функции 'export_to_dict';")
    def test_returned_params():
        """
        Тест, проверяющий количество собранных параметров.
        """
        system_params = inspector.export_to_dict()
        assert isinstance(system_params, dict), \
            f"Error - wrong returned type!\n \
            Expected - dict, returned - {type(system_params)}"
    