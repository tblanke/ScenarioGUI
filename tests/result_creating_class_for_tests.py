from __future__ import annotations
from collections.abc import Callable

from matplotlib import pyplot as plt


class ResultsClass:
    def __init__(self, a: int = 1, b: int = 2):
        self.a = a
        self.b = b
        self.result = None

    def adding(self):
        self.result = self.a + self.b

    def subtract(self):
        if self.a > 190:
            raise ValueError("Value above 190")
        self.result = self.a - self.b

    def get_result(self) -> float:
        return self.result

    def create_plot(self, legend: bool = False) -> tuple[plt.Figure, plt.Axes]:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # set axes labels
        ax.set_xlabel(r"Time (year)")
        ax.set_ylabel(r"Temperature ($^\circ C$)")
        ax.hlines(self.a, 0, self.b, colors="r", linestyles="dashed", label="line", lw=1)
        if legend:
            ax.legend()
        return fig, ax

    def to_dict(self) -> dict:
        return {"a": self.a, "b": self.b, "result": self.result}

    @staticmethod
    def from_dict(dictionary: dict) -> ResultsClass:
        res = ResultsClass()
        res.a = dictionary["a"]
        res.b = dictionary["b"]
        res.result = dictionary["result"]
        return res


def data_2_results(data) -> tuple[ResultsClass, Callable[[], None]]:
    result = ResultsClass(data.int_a, data.float_b)
    return result, result.adding if data.aim_add else result.subtract
