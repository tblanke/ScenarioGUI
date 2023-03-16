from typing import Callable

from matplotlib import pyplot as plt


class ResultsClass:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b
        self.result = None

    def adding(self):
        self.result = self.a + self.b

    def subtract(self):
        if self.a > 190:
            raise ValueError
        self.result = self.a - self.b

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

    def _to_dict(self) -> dict:
        return {"a" : self.a, "b": self.b, "result": self.result}

    def _from_dict(self, dictionary: dict):
        self.a = dictionary["a"]
        self.b = dictionary["b"]
        self.result = dictionary["result"]


def data_2_results(data) -> tuple[ResultsClass, Callable[[], None]]:
    result = ResultsClass(data.int_a, data.float_b)
    return result, result.adding if data.aim_add else result.subtract
