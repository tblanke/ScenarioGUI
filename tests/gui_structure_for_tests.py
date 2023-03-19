from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

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
    ListBox,
    Page,
    ResultFigure,
    ResultText, TextBox,
)

if TYPE_CHECKING:
    import PySide6.QtWidgets as QtW

    from .test_translations.translation_class import Translations


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

        self.function_button = FunctionButton(button_text="function", icon="Add", category=self.category_inputs)

        self.button_box = ButtonBox(label="a or b?", default_index=0, entries=["a", "b"], category=self.category_inputs)

        self.list_box = ListBox(
            label="List box",
            default_index=0,
            entries=["0", "1", "2", "3"],
            category=self.category_inputs,
        )

        self.text_box = TextBox(label="Login", default_text="Example text 15", category=self.category_inputs)

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
        self.list_small_2 = ListBox(
            label="",
            default_index=0,
            entries=["0", "1", "2", "3"],
            category=self.category_grid,
        )
        self.text_box_small = TextBox(label="", default_text="Example text 15", category=self.category_grid, password=True)
        self.category_grid.activate_graphic_left()
        self.category_grid.activate_graphic_right()

        self.button_box.add_link_2_show(self.hint_1, on_index=1)
        self.list_small_2.add_link_2_show(self.hint_2, on_index=1)
        self.aim_add.add_link_2_show(self.int_small_2)

        self.int_small_2.add_aim_option_2_be_set_for_check(self.aim_plot)
        self.float_small_1.add_aim_option_2_be_set_for_check(self.aim_add)

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

        self.counter = 0
        self.page_inputs.add_function_called_if_button_clicked(self.count)

    def count(self):
        self.counter += 1
