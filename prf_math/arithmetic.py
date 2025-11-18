from .core import *


class PredecessorFunction(PRFFunction):
    def __init__(self):
        super().__init__("pred", 1)

    def evaluate(self, args: List[int]) -> int:
        x = args[0]
        return 0 if x == 0 else x - 1


class MonusFunction(PRFFunction):
    def __init__(self):
        super().__init__("monus", 2)

    def evaluate(self, args: List[int]) -> int:
        x, y = args
        if y == 0:
            return x
        pred_x = 0 if x == 0 else x - 1
        pred_y = 0 if y == 0 else y - 1
        return self.evaluate([pred_x, pred_y])


class AdditionFunction(PRFFunction):
    def __init__(self):
        super().__init__("add", 2)

    def evaluate(self, args: List[int]) -> int:
        x, y = args
        if y == 0:
            return x
        return self.evaluate([x, y - 1]) + 1


class MultiplicationFunction(PRFFunction):
    def __init__(self):
        super().__init__("mult", 2)
        self.add = AdditionFunction()

    def evaluate(self, args: List[int]) -> int:
        x, y = args
        if y == 0:
            return 0
        return self.add.evaluate([x, self.evaluate([x, y - 1])])


class IsZeroFunction(PRFFunction):
    def __init__(self):
        super().__init__("is_zero", 1)

    def evaluate(self, args: List[int]) -> int:
        return 1 if args[0] == 0 else 0


class LessOrEqualFunction(PRFFunction):
    def __init__(self):
        super().__init__("leq", 2)
        self.monus = MonusFunction()
        self.is_zero = IsZeroFunction()

    def evaluate(self, args: List[int]) -> int:
        x, y = args
        diff = self.monus.evaluate([x, y])
        return self.is_zero.evaluate([diff])


class ConditionalFunction(PRFFunction):
    def __init__(self):
        super().__init__("cond", 3)

    def evaluate(self, args: List[int]) -> int:
        condition, true_val, false_val = args
        return true_val if condition == 1 else false_val


class MinimumFunction(PRFFunction):
    """Минимум двух чисел: min(x, y)"""
    def __init__(self):
        super().__init__("min", 2)
        self.leq = LessOrEqualFunction()
        self.cond = ConditionalFunction()

    def evaluate(self, args: List[int]) -> int:
        x, y = args
        # min(x, y) = x если x ≤ y, иначе y
        if self.leq.evaluate([x, y]) == 1:
            return x
        else:
            return y


class MaximumFunction(PRFFunction):
    """Максимум двух чисел: max(x, y)"""
    def __init__(self):
        super().__init__("max", 2)
        self.leq = LessOrEqualFunction()
        self.cond = ConditionalFunction()

    def evaluate(self, args: List[int]) -> int:
        x, y = args
        # max(x, y) = x если x ≥ y, иначе y
        if self.leq.evaluate([y, x]) == 1:  # y ≤ x значит x ≥ y
            return x
        else:
            return y


class AndFunction(PRFFunction):
    """Логическое И: and(x, y) = 1 если x=1 и y=1, иначе 0"""
    def __init__(self):
        super().__init__("and", 2)
        self.mult = MultiplicationFunction()

    def evaluate(self, args: List[int]) -> int:
        x, y = args
        # and(x, y) = 1 если x=1 и y=1, иначе 0
        return 1 if x == 1 and y == 1 else 0


class EqualsFunction(PRFFunction):
    """Проверка равенства: equals(x, y) = 1 если x=y, иначе 0"""
    def __init__(self):
        super().__init__("equals", 2)
        self.is_zero = IsZeroFunction()
        self.monus = MonusFunction()
        self.and_func = AndFunction()

    def evaluate(self, args: List[int]) -> int:
        x, y = args
        # x = y тогда и только тогда, когда (x ∸ y) = 0 и (y ∸ x) = 0
        diff1 = self.monus.evaluate([x, y])
        diff2 = self.monus.evaluate([y, x])
        zero1 = self.is_zero.evaluate([diff1])
        zero2 = self.is_zero.evaluate([diff2])
        return self.and_func.evaluate([zero1, zero2])