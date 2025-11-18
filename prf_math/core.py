from abc import ABC, abstractmethod
from typing import List


class PRFFunction(ABC):
    def __init__(self, name: str, arity: int):
        self.name = name
        self.arity = arity

    @abstractmethod
    def evaluate(self, args: List[int]) -> int:
        pass

    def __call__(self, *args):
        return self.evaluate(list(args))


class ZeroFunction(PRFFunction):
    def __init__(self):
        super().__init__("Z", 1)

    def evaluate(self, args: List[int]) -> int:
        return 0


class SuccessorFunction(PRFFunction):
    def __init__(self):
        super().__init__("S", 1)

    def evaluate(self, args: List[int]) -> int:
        return args[0] + 1


class ProjectionFunction(PRFFunction):
    def __init__(self, n: int, i: int):
        super().__init__(f"P_{i}^{n}", n)
        self.index = i - 1

    def evaluate(self, args: List[int]) -> int:
        return args[self.index]


class CompositionFunction(PRFFunction):
    def __init__(self, f: PRFFunction, g_functions: List[PRFFunction]):
        arity = g_functions[0].arity
        super().__init__("composition", arity)
        self.f = f
        self.g_functions = g_functions

    def evaluate(self, args: List[int]) -> int:
        g_results = [g.evaluate(args) for g in self.g_functions]
        return self.f.evaluate(g_results)


class PrimitiveRecursionFunction(PRFFunction):
    def __init__(self, g: PRFFunction, h: PRFFunction):
        super().__init__("prim_rec", g.arity + 1)
        self.g = g
        self.h = h

    def evaluate(self, args: List[int]) -> int:
        n = args[0]
        other_args = args[1:]

        if n == 0:
            return self.g.evaluate(other_args)

        prev_result = self.evaluate([n - 1] + other_args)
        h_args = [n - 1, prev_result] + other_args
        return self.h.evaluate(h_args)