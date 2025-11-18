from .arithmetic import *


class GCDFunction(PRFFunction):
    def __init__(self):
        super().__init__("strict_gcd", 2)
        self.min = MinimumFunction()
        self.equals = EqualsFunction()
        self.monus = MonusFunction()
        self.is_zero = IsZeroFunction()
        self.and_func = AndFunction()

    def evaluate(self, args: List[int]) -> int:
        a, b = args
        # Если одно из чисел 0, возвращаем другое
        if a == 0:
            return b
        if b == 0:
            return a
        # Ищем наибольший делитель от min(a,b) вниз до 1
        max_possible = self.min.evaluate([a, b])
        return self._find_gcd(a, b, max_possible)

    def _find_gcd(self, a: int, b: int, candidate: int) -> int:
        """Рекурсивно ищем наибольший общий делитель"""
        # Базовый случай: candidate = 1 всегда делит любые числа
        if candidate == 1:
            return 1
        # Проверяем, делит ли candidate оба числа
        if self._divides(candidate, a) and self._divides(candidate, b):
            return candidate
        # Рекурсивно проверяем следующего кандидата
        return self._find_gcd(a, b, candidate - 1)

    def _divides(self, d: int, n: int) -> bool:
        """Проверяет, делит ли d число n (d | n)"""
        if d == 0:
            return False
        # d делит n, если существует k такое, что k * d = n
        # Это эквивалентно тому, что n mod d = 0
        remainder = n
        while remainder >= d:
            remainder = self.monus.evaluate([remainder, d])
        return self.equals.evaluate([remainder, 0]) == 1


class DivisionFunction(PRFFunction):
    def __init__(self):
        super().__init__("prf_div", 2)
        self.monus = MonusFunction()
        self.is_zero = IsZeroFunction()

    def evaluate(self, args: List[int]) -> int:
        x, y = args
        if self.is_zero.evaluate([y]) == 1:
            return 0
        # Ограничиваем количество шагов
        max_steps = x  # Максимум x шагов
        return self._bounded_div(x, y, max_steps)

    def _bounded_div(self, x: int, y: int, steps: int) -> int:
        """Деление с ограниченным количеством шагов"""
        if steps == 0:
            return 0
        if x >= y:
            # quotient = 1 + division(x-y, y)
            return 1 + self._bounded_div(
                self.monus.evaluate([x, y]),
                y,
                steps - 1
            )
        else:
            return 0


class LCMFunction(PRFFunction):
    def __init__(self):
        super().__init__("lcm", 2)
        self.mult = MultiplicationFunction()
        self.gcd = GCDFunction()
        self.div = DivisionFunction()

    def evaluate(self, args: List[int]) -> int:
        a, b = args
        if a == 0 or b == 0:
            return 0

        product = self.mult.evaluate([a, b])
        gcd_val = self.gcd.evaluate([a, b])
        return self.div.evaluate([product, gcd_val])