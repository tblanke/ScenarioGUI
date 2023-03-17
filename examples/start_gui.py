"""
script to start the GUI
"""
# pragma: no cover
from __future__ import annotations

import sys
from pathlib import Path
from platform import system
from sys import argv
from typing import TYPE_CHECKING

from matplotlib import pyplot as plt

import ScenarioGUI.global_settings as global_vars
from examples.translation_class import Translations
from ScenarioGUI.global_settings import FILE_EXTENSION, GUI_NAME
from ScenarioGUI.gui_classes.gui_structure import GuiStructure
from ScenarioGUI.gui_classes.gui_structure_classes import (
    Aim,
    ButtonBox,
    Category,
    FigureOption,
    FileNameBox,
    FloatBox,
    FunctionButton,
    Hint,
    IntBox,
    Page,
    ResultFigure,
    ResultText,
)

if TYPE_CHECKING:
    import PySide6.QtWidgets as QtW
    from collections.abc import Callable

os_system = system()
is_frozen = getattr(sys, "frozen", False) and os_system == "Windows"  # pragma: no cover


class ResultsClass:
    def __init__(self, a: int = 1, b: int = 2):
        self.a = a
        self.b = b
        self.result = None

    def adding(self):
        self.result = self.a + self.b

    def subtract(self):
        if self.a > 190:
            raise ValueError
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

    def _to_dict(self) -> dict:
        return {"a": self.a, "b": self.b, "result": self.result}

    def _from_dict(self, dictionary: dict):
        self.a = dictionary["a"]
        self.b = dictionary["b"]
        self.result = dictionary["result"]


class GUI(GuiStructure):
    def __init__(self, default_parent: QtW.QWidget, translations: Translations):
        super().__init__(default_parent, translations)
        self.page_inputs = Page(name="Inputs", button_name="Inputs", icon="Add.svg")
        self.aim_add = Aim(label="Adding", icon="Add", page=self.page_inputs)
        self.aim_sub = Aim(label="Substract", icon="Delete", page=self.page_inputs)
        self.aim_plot = Aim(label="Plot", icon="Parameters", page=self.page_inputs)
        self.category_inputs = Category(page=self.page_inputs, label="Inputs")
        self.int_a = IntBox(
            label="a",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            category=self.category_inputs,
        )

        self.float_b = FloatBox(
            label="b",
            default_value=100,
            minimal_value=0,
            maximal_value=1000,
            decimal_number=2,
            category=self.category_inputs,
        )
        folder: Path = Path(__file__).parent
        file = f'{folder.joinpath("./example_data.csv")}'
        self.filename = FileNameBox(label="Filename", default_value=file, category=self.category_inputs, dialog_text="Hello", error_text="no file found")

        self.button_box = ButtonBox(label="a or b?", default_index=0, entries=["a", "b"], category=self.category_inputs)

        self.function_button = FunctionButton(button_text="function", icon="Add", category=self.category_inputs)

        self.button_box = ButtonBox(label="a or b?", default_index=0, entries=["a", "b"], category=self.category_inputs)

        self.category_grid = Category(page=self.page_inputs, label="Grid")
        self.category_grid.activate_grid_layout(3)
        self.hint_1 = Hint(category=self.category_grid, hint="Grid example")
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.int_small_1 = IntBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            category=self.category_grid,
        )
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.float_small_1 = FloatBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            decimal_number=2,
            category=self.category_grid,
        )
        self.hint_2 = Hint(category=self.category_grid, hint="Grid example")
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.int_small_2 = IntBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            category=self.category_grid,
        )
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.float_small_2 = FloatBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            decimal_number=2,
            category=self.category_grid,
        )
        self.category_grid.activate_graphic_left()
        self.category_grid.activate_graphic_right()

        self.create_results_page()
        self.numerical_results = Category(page=self.page_result, label="Numerical results")

        self.result_text_add = ResultText("Result", category=self.numerical_results, prefix="Result: ", suffix="m")
        self.result_text_add.text_to_be_shown("ResultsClass", "get_result")
        self.result_text_add.function_to_convert_to_text(lambda x: round(x, 2))
        self.result_text_sub = ResultText("Result", category=self.numerical_results, prefix="Result: ", suffix="m")
        self.result_text_sub.text_to_be_shown("ResultsClass", "result")
        self.result_text_sub.function_to_convert_to_text(lambda x: round(x, 2))

        self.figure_results = ResultFigure(label="Plot", page=self.page_result)
        self.legend_figure_results = FigureOption(
            category=self.figure_results, label="Legend on", param="legend", default=0, entries=["No", "Yes"], entries_values=[False, True]
        )

        self.figure_results.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot")

        self.aim_add.add_link_2_show(self.result_text_add)
        self.aim_sub.add_link_2_show(self.result_text_sub)
        self.aim_plot.add_link_2_show(self.figure_results)

        self.create_settings_page()
        self.create_lists()
        self.page_inputs.set_next_page(self.page_result)
        self.page_result.set_previous_page(self.page_inputs)
        self.page_result.set_next_page(self.page_settings)
        self.page_result.set_previous_page(self.page_result)


def data_2_results(data) -> tuple[ResultsClass, Callable[[], None]]:
    result = ResultsClass(data.int_a, data.float_b)
    return result, result.adding if data.aim_add else result.subtract

global_vars.FONT = "Arial"
global_vars.FONT_SIZE = 12
global_vars.FILE_EXTENSION = "tool"
global_vars.DARK = "rgb(0,0,0)"
global_vars.LIGHT = "rgb(255,204,0)"
global_vars.GUI_NAME = "My GUI name"
global_vars.ICON_NAME = "icon"
global_vars.VERSION = "0.2.0"
folder = Path("__file__").parent
global_vars.FOLDER = folder
global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def run(path_list=None):  # pragma: no cover
    if is_frozen:
        import pyi_splash

        pyi_splash.update_text("Loading .")
    from sys import exit as sys_exit

    if is_frozen:
        pyi_splash.update_text("Loading ..")

    from PySide6.QtWidgets import QApplication as QtWidgets_QApplication
    from PySide6.QtWidgets import QMainWindow as QtWidgets_QMainWindow

    from ScenarioGUI.global_settings import VERSION
    from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

    if is_frozen:
        pyi_splash.update_text("Loading ...")

    # init application
    app = QtWidgets_QApplication()
    # set version and id
    my_app_id = f"{GUI_NAME} v{VERSION}"  # arbitrary string
    if os_system == "Windows":
        from ctypes import windll as ctypes_windll

        ctypes_windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
    app.setApplicationName(GUI_NAME)
    app.setApplicationVersion(f"v{VERSION}")
    # init window
    window = QtWidgets_QMainWindow()
    # init gui window
    main_window = MainWindow(window, app, GUI, Translations)
    if is_frozen:
        pyi_splash.update_text("Loading ...")
    # load file if it is in path list
    if path_list is not None:
        main_window.filename = (
            [path for path in path_list if path.endswith(f".{FILE_EXTENSION}")][0],
            0,
        )
        main_window.fun_load_known_filename()

    # show window
    if is_frozen:
        pyi_splash.close()
    window.showMaximized()
    # close app
    sys_exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    # pass system args like a file to read
    run(argv if len(argv) > 1 else None)
