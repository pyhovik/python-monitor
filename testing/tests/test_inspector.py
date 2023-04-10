"""
Тест-набор для тестирования функций модуля "inspector".
"""
import allure
from app.modules.inspector import Inspector

inspector = Inspector()


class TestInspector:
    
    def test_returned_params(self):
        """
        Тест, проверяющий количество собранных параметров.
        """
        system_params = inspector.export_to_dict()
        assert isinstance(system_params, dict), \
            f"Error - wrong returned type!\n \
            Expected - dict, returned - {type(system_params)}"
    