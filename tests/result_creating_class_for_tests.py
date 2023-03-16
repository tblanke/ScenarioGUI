from typing import Callable


class ResultsClass:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b
        self.result = None

    def adding(self):
        self.result = self.a + self.b

    def subtract(self):
        self.result = self.a - self.b

    def _to_dict(self) -> dict:
        return {"a" : self.a, "b": self.b, "result": self.result}

    def _from_dict(self, dictionary: dict):
        self.a = dictionary["a"]
        self.b = dictionary["b"]
        self.result = dictionary["result"]


def data_2_results(data) -> tuple[ResultsClass, Callable[[], None]]:
    result = ResultsClass(data.int_a, data.int_b)
    return result, result.adding if data.aim_add else result.subtract
