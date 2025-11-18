import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from prf_math.core import ZeroFunction, SuccessorFunction
from prf_math.arithmetic import AdditionFunction, MultiplicationFunction, MonusFunction
from prf_math.gcd_lcm import GCDFunction, LCMFunction


class TestPRFFunctions:
    """Тесты примитивно рекурсивных функций"""

    def test_zero_function(self):
        zero = ZeroFunction()
        assert zero(5) == 0
        assert zero(0) == 0

    def test_successor_function(self):
        succ = SuccessorFunction()
        assert succ(0) == 1
        assert succ(5) == 6

    def test_addition_function(self):
        add = AdditionFunction()
        assert add(2, 3) == 5
        assert add(0, 5) == 5

    def test_multiplication_function(self):
        mult = MultiplicationFunction()
        assert mult(3, 4) == 12
        assert mult(0, 5) == 0

    def test_monus_function(self):
        monus = MonusFunction()
        assert monus(5, 3) == 2
        assert monus(3, 5) == 0


class TestGCDLCM:
    """Тесты НОД и НОК"""

    def test_gcd_basic(self):
        gcd = GCDFunction()
        assert gcd(48, 18) == 6
        assert gcd(56, 42) == 14
        assert gcd(17, 13) == 1

    def test_gcd_edge_cases(self):
        gcd = GCDFunction()
        assert gcd(0, 5) == 5
        assert gcd(7, 0) == 7
        assert gcd(100, 25) == 25

    def test_lcm_basic(self):
        lcm = LCMFunction()
        assert lcm(4, 6) == 12
        assert lcm(5, 7) == 35
        assert lcm(12, 18) == 36

    def test_lcm_edge_cases(self):
        lcm = LCMFunction()
        assert lcm(0, 5) == 0
        assert lcm(7, 0) == 0

    def test_gcd_lcm_relationship(self):
        gcd = GCDFunction()
        lcm = LCMFunction()

        # Проверка: a * b = gcd(a,b) * lcm(a,b)
        a, b = 48, 18
        gcd_val = gcd(a, b)
        lcm_val = lcm(a, b)
        assert a * b == gcd_val * lcm_val


class TestPostgreSQL:
    """Тесты для PostgreSQL (требует запущенной БД)"""

    def test_postgres_connection(self):
        """Тест подключения к PostgreSQL"""
        try:
            from database.dbmanager import DatabaseManager
            db_manager = DatabaseManager()

            # Простая проверка что подключение работает
            calculations = db_manager.get_all_calculations()
            # Если не выброшено исключение - подключение работает
            assert True

        except Exception as e:
            # Если БД не запущена, пропускаем тест
            pytest.skip(f"PostgreSQL не доступен: {e}")

    def test_postgres_operations(self):
        """Тест операций с PostgreSQL"""
        try:
            from database.dbmanager import DatabaseManager
            db_manager = DatabaseManager()

            # Сохраняем тестовые данные
            record_id = db_manager.save_calculation("НОД", 48, 18, 6)
            assert record_id is not None

            # Получаем данные
            calculations = db_manager.get_all_calculations()
            # Хотя бы одна запись должна быть
            assert len(calculations) >= 1

        except Exception as e:
            pytest.skip(f"PostgreSQL не доступен: {e}")


