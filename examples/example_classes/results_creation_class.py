from __future__ import annotations

from matplotlib import pyplot as plt


class ResultsClass:  # pragma: no cover
    def __init__(self, a: int = 1, b: int = 2):
        self.a = a
        self.b = b
        self.result = None

    def adding(self):
        # loop over 1_000_000 to take some time
        self.result = 0
        for i in range(50_000_000):
            self.result += i
        self.result = self.a + self.b

    def subtract(self):
        if self.a > 190:
            raise ValueError
        self.result = self.a - self.b

    def get_result(self) -> float:
        return self.result

    def export(self, filename: str):
        with open(filename, "w") as file:
            file.write(f"result: {self.result}")

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

    def create_plot_multiple_lines(self, legend: bool = False) -> tuple[plt.Figure, plt.Axes]:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # set axes labels
        ax.set_xlabel(r"Time (year)")
        ax.set_ylabel(r"Temperature ($^\circ C$)")
        ax.hlines(self.a, 0, self.b, colors="r", linestyles="dashed", label="line", lw=1)
        ax.hlines(self.a * 2, 0, self.b, colors="b", linestyles="dashed", label="line", lw=1)

        if legend:
            ax.legend()
        return fig, ax

    def to_dict(self) -> dict:
        return {"a": self.a, "b": self.b, "result": self.result}

    @staticmethod
    def from_dict(dictionary: dict) -> ResultsClass:
        res = ResultsClass(dictionary["a"], dictionary["b"])
        res.result = dictionary["result"]
        return res
