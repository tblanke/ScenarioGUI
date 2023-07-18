from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING

from ScenarioGUI import GuiStructure
from ScenarioGUI import elements as els
from ScenarioGUI.gui_classes.gui_structure_classes import (
    Aim,
    ButtonBox,
    Category,
    FigureOption,
    FileNameBox,
    FlexibleAmount,
    FloatBox,
    FunctionButton,
    Hint,
    IntBox,
    ListBox,
    Page,
    ResultExport,
    ResultFigure,
    ResultText,
    TextBox,
)

if TYPE_CHECKING:
    import PySide6.QtWidgets as QtW

    from .test_translations.translation_class import Translations


class GUI(GuiStructure):
    def __init__(self, default_parent: QtW.QWidget, translations: Translations):
        super().__init__(default_parent, translations)
        self.page_inputs = Page(name="Inputs", button_name="Inputs", icon="Add.svg")
        self.aim_add = Aim(label=self.translations.aim_add, icon="Add", page=self.page_inputs)
        self.aim_sub = Aim(label=self.translations.aim_sub, icon="Delete", page=self.page_inputs)
        self.aim_plot = Aim(label="Plot", icon="Parameters", page=self.page_inputs)
        self.aim_last = Aim(label="Last", icon="Parameters", page=self.page_inputs)
        # set three aims per row
        self.page_inputs.aims_in_row = 4
        self.category_inputs = Category(page=self.page_inputs, label="Inputs")
        self.int_a = IntBox(
            label="a",
            default_value=2,
            minimal_value=0,
            maximal_value=300,
            category=self.category_inputs,
        )

        self.sub_category = els.Subcategory("Subcategory", self.category_inputs)

        self.float_a = els.FloatBox(
            label="a",
            default_value=100,
            minimal_value=0,
            maximal_value=1000,
            decimal_number=2,
            category=self.sub_category,
        )
        self.float_c = els.FloatBox(
            label="c",
            default_value=100,
            minimal_value=0,
            maximal_value=1000,
            decimal_number=2,
            category=self.sub_category,
        )
        self.float_d = els.FloatBox(
            label="d",
            default_value=100,
            minimal_value=0,
            maximal_value=1000,
            decimal_number=2,
            category=self.sub_category,
        )

        self.float_b = els.FloatBox(
            label="b",
            default_value=100,
            minimal_value=0,
            maximal_value=1000,
            decimal_number=2,
            category=self.sub_category,
        )

        self.int_units = els.IntBoxWithUnits(
            label="IntBoxWithUnits",
            default_value=2,
            minimal_value=0,
            maximal_value=2_000_000,
            category=self.category_inputs,
            units=[("kW", 1), ("W", 0.001), ("MW", 1_000)]
        )

        self.int_a.change_event(self.disable_aim(self.aim_sub, self.page_inputs, partial(self.int_a.check_linked_value, (None, 200))))
        self.float_b.change_event(self.disable_aim(self.aim_add, self.page_inputs, partial(self.float_b.check_linked_value, (30, None))))
        self.int_units.change_event(self.disable_aim(self.aim_plot, self.page_inputs, partial(self.int_units.check_linked_value, (None, 20))))

        self.result_text_not_on_result_page = els.ResultText("Result not on result page", self.category_inputs,
                                                             prefix="OK", suffix="Suf")

        self.float_units = els.FloatBoxWithUnits(
            label="FloatBoxWithUnits",
            default_value=2,
            minimal_value=0,
            maximal_value=2_000_000,
            decimal_number=2,
            category=self.category_inputs,
            units=[("kW", 1), ("W", 0.001), ("MW", 1_000)]
        )
        self.float_units.activate_scale_decimals()
        folder: Path = Path(__file__).parent
        file = f'{folder.joinpath("./example_data.csv")}'
        self.filename = FileNameBox(label="Filename", default_value=file, category=self.category_inputs, dialog_text="Hello", error_text="no file found")
        self.filename.check_active = True

        self.function_button = FunctionButton(button_text=translations.function_button, icon="Add", category=self.category_inputs)

        self.button_box = els.ButtonBox(label="a or b or c?", default_index=0, entries=["a", "b", "c"], category=self.category_inputs)
        self.button_box.add_link_2_show(self.filename, on_index=1)

        self.aim_plot.widget.toggled.connect(self.disable_button_box(self.button_box, at_index=2, func_2_check=self.aim_plot.widget.isChecked))
        self.float_b.change_event(self.disable_button_box(self.button_box, 1, partial(self.float_b.check_linked_value, (50, None))))
        self.int_a.change_event(self.disable_button_box(self.button_box, 0, partial(self.int_a.check_linked_value, (None, 10))))

        self.button_box_short = els.ButtonBox(label="b or c?", default_index=0, entries=["b", "c"], category=self.category_inputs)
        self.float_b.change_event(self.disable_button_box(self.button_box_short, 1, partial(self.float_b.check_linked_value, (50, None))))
        self.int_a.change_event(self.disable_button_box(self.button_box_short, 0, partial(self.int_a.check_linked_value, (None, 10))))

        self.aim_plot.add_link_2_show(self.button_box)

        self.list_box = ListBox(
            label="List box",
            default_index=0,
            entries=["0", "1", "2", "3"],
            category=self.category_inputs,
        )
        self.text_box_only_on_add = els.TextBox(label="Only visible on add", default_text="Hello", category=self.category_inputs)

        self.aim_add.add_link_2_show(self.text_box_only_on_add)

        self.text_box = TextBox(label="Login", default_text="Example text 15", category=self.category_inputs)
        self.text_box_multi_line = els.TextBoxMultiLine(label="Example Multi Line", default_text="Hello\nmulti line", category=self.category_inputs)
        
        self.flex_option = FlexibleAmount(label="layers", default_length=2, entry_mame="Layer", category=self.category_inputs,
                                          default_values=[["layer 1", 9.5, 3, 2], ["layer 2", 10.5, 2, 1]])
        self.flex_option.add_option(TextBox, name="name", default_text="layer")
        self.flex_option.add_option(FloatBox, name="thickness", default_value=10, minimal_value=5, decimal_number=2)
        self.flex_option.add_option(IntBox, name="amount", default_value=4, minimal_value=2)
        self.flex_option.add_option(ListBox, name="entry", default_index=0, entries=["entry 1", "entry 2", "entry 3"])
        self.hint_flex = Hint(hint="wrong length of flexible option", category=self.category_inputs, warning=True)
        self.flex_option.add_link_2_show(self.hint_flex, 4, 12)

        self.multiple_ints = els.MultipleIntBox(label="Multiple int box:", category=self.category_inputs, default_value=(1, 2, 3), minimal_value=(1, 1, 1),
                                                maximal_value=(100, 110, 120))

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
        self.font_style = els.FontListBox(label="Font label", category=self.category_grid, entries=["Arial", "Verdana"], default_index=0)
        self.multiple_ints_small = els.MultipleIntBox(label="Multiple int box:", category=self.category_grid, default_value=(1, 2, 3), minimal_value=(1, 1,
                                                                                                                                                        1),
                                                maximal_value=(100, 110, 120))

        self.text_box_multi_line_small = els.TextBoxMultiLine(label="Example Multi Line", default_text="Hello\nmulti line", category=self.category_grid)
        self.category_grid.activate_graphic_left()
        self.category_grid.activate_graphic_right()

        self.button_box.add_link_2_show(self.hint_1, on_index=1)
        self.list_small_2.add_link_2_show(self.hint_2, on_index=1)
        self.aim_add.add_link_2_show(self.int_small_2)

        self.int_small_2.add_aim_option_2_be_set_for_check(self.aim_plot)
        self.float_small_1.add_aim_option_2_be_set_for_check(self.aim_add)

        self.create_results_page()
        self.numerical_results = Category(page=self.page_result, label=["Numerical results"])

        self.result_text_add = ResultText("Result", category=self.numerical_results, prefix="Result: ", suffix="m")
        self.result_text_add.text_to_be_shown("ResultsClass", "get_result")
        self.result_text_add.function_to_convert_to_text(lambda x: round(x, 2))
        self.result_text_sub = ResultText("Result", category=self.numerical_results, prefix="Result: ", suffix="m")
        self.result_text_sub.text_to_be_shown("ResultsClass", "result")
        self.result_text_sub.function_to_convert_to_text(lambda x: round(x, 2))

        self.export_results = ResultExport(
            "Export", icon="Download", category=self.numerical_results, export_function="export", caption="Please select file", file_extension="txt"
        )

        self.figure_results = ResultFigure(label=self.translations.figure_results, page=self.page_result)
        self.legend_figure_results = FigureOption(
            category=self.figure_results, label=["Show legend?"], param="legend", default=0, entries=["No", "Yes"], entries_values=[False, True]
        )

        self.figure_results.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot")
        self.figure_results_with_different_other_saved_figure = els.ResultFigure(label=self.translations.figure_results,
                                                                                 page=self.page_result, x_axes_text="X-Axes", y_axes_text="Y-Axes",
                                                                                 customizable_figure=1)
        self.legend_figure_results_with_other_saved_figure = els.FigureOption(
            category=self.figure_results_with_different_other_saved_figure, label="Legend on", param="legend", default=0, entries=["No", "Yes"],
            entries_values=[False, True]
        )

        self.figure_results_with_different_other_saved_figure.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot")

        self.figure_results_with_customizable_layout = els.ResultFigure(label=self.translations.figure_results, page=self.page_result,
                                                                        x_axes_text="X-Axes", y_axes_text="Y-Axes", customizable_figure=2)
        self.legend_figure_results_with_customizable_layout = els.FigureOption(
            category=self.figure_results_with_customizable_layout, label="Legend on", param="legend", default=0, entries=["No", "Yes"],
            entries_values=[False, True]
        )

        self.figure_results_with_customizable_layout.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot")

        self.figure_results.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot")

        self.aim_add.add_link_2_show(self.result_text_add)
        self.aim_sub.add_link_2_show(self.result_text_sub)
        self.aim_plot.add_link_2_show(self.figure_results)

        self.aim_add.add_link_2_show(self.figure_results_with_different_other_saved_figure)
        self.aim_sub.add_link_2_show(self.figure_results_with_different_other_saved_figure)
        self.aim_plot.add_link_2_show(self.figure_results_with_different_other_saved_figure)

        self.aim_add.add_link_2_show(self.figure_results_with_customizable_layout)
        self.aim_sub.add_link_2_show(self.figure_results_with_customizable_layout)
        self.aim_plot.add_link_2_show(self.figure_results_with_customizable_layout)

        self.create_settings_page()
        self.create_lists()

        self.page_inputs.set_next_page(self.page_result)
        self.page_result.set_previous_page(self.page_inputs)
        self.page_result.set_next_page(self.page_settings)

        self.counter = 0
        self.page_inputs.add_function_called_if_button_clicked(self.count)

    def count(self):
        self.counter += 1
