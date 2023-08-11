from __future__ import annotations

import logging
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING

from ScenarioGUI import GuiStructure
from ScenarioGUI import elements as els

from .results_creation_class import ResultsClass

if TYPE_CHECKING:
    import PySide6.QtWidgets as QtW

    from .translation_class import Translations


class GUI(GuiStructure):
    def __init__(self, default_parent: QtW.QWidget, translations: Translations):
        super().__init__(default_parent, translations)
        self.page_inputs = els.Page(name=translations.page_inputs, button_name="Inputs", icon="Add.svg")
        self.page_inputs1 = els.Page(name=translations.page_inputs, button_name="Inputs", icon="Add.svg")
        self.page_inputs2 = els.Page(name=translations.page_inputs, button_name="Inputs", icon="Add.svg")
        self.page_export = els.Page(name=translations.page_output, button_name="Output", icon="Delete.svg")
        self.aim_add = els.Aim(label="Adding", icon="Add", page=self.page_inputs)
        self.aim_sub = els.Aim(label="Substract", icon="Delete", page=self.page_inputs)
        self.aim_plot = els.Aim(label="Plot", icon="Parameters", page=self.page_inputs)
        # this three aims can appear in one row by setting:
        self.page_inputs.aims_in_row = 3
        self.category_inputs = els.Category(page=self.page_inputs, label="Inputs")
        self.int_a = els.IntBox(
            label="a",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            category=self.category_inputs,
        )
        self.int_a.change_event(
            self.disable_aim(
                self.aim_sub,
                self.page_inputs,
                partial(self.int_a.check_linked_value, (None, 5)),
            )
        )

        self.int_units = els.IntBoxWithUnits(
            label="IntBoxWithUnits",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            category=self.category_inputs,
            units=[("kW", 1), ("W", 0.001), ("MW", 1_000)],
        )

        self.float_units = els.FloatBoxWithUnits(
            label="FloatBoxWithUnits",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            decimal_number=2,
            category=self.category_inputs,
            units=[("kW", 1), ("W", 0.001), ("MW", 1_000)],
        )
        self.float_units.activate_scale_decimals()

        self.sub_category = els.Subcategory("Subcategory", self.category_inputs)

        self.float_b = els.FloatBox(
            label="b",
            default_value=100,
            minimal_value=0,
            maximal_value=1000,
            decimal_number=2,
            category=self.sub_category,
        )

        self.list_box = els.ListBox(
            label="List box",
            default_index=0,
            category=self.category_inputs,
            entries=["1", "2", "3", "4"],
        )
        folder: Path = Path(__file__).parent
        file = f'{folder.joinpath("./example_data.csv")}'
        self.filename = els.FileNameBox(
            label="Filename",
            default_value=file,
            category=self.category_inputs,
            dialog_text="Hello",
            error_text="no file found",
            file_extension=["txt", "csv"],
        )

        self.text_box_only_on_add = els.TextBox(
            label="Only visible on add",
            default_text="Hello",
            category=self.category_inputs,
        )

        self.aim_add.add_link_2_show(self.text_box_only_on_add)
        # self.aim_add.add_link_2_show(self.filename)
        self.button_box = els.ButtonBox(
            label="a or b or c?",
            default_index=0,
            entries=["a", "b", "c"],
            category=self.category_inputs,
        )

        self.aim_plot.widget.toggled.connect(self.disable_button_box(self.button_box, at_index=2, func_2_check=self.aim_plot.widget.isChecked))
        self.float_b.change_event(self.disable_button_box(self.button_box, 1, partial(self.float_b.check_linked_value, (50, None))))
        self.int_a.change_event(self.disable_button_box(self.button_box, 0, partial(self.int_a.check_linked_value, (None, 10))))

        self.button_box_short = els.ButtonBox(
            label="b or c?",
            default_index=0,
            entries=["b", "c"],
            category=self.category_inputs,
        )
        self.float_b.change_event(
            self.disable_button_box(
                self.button_box_short,
                1,
                partial(self.float_b.check_linked_value, (50, None)),
            )
        )
        self.int_a.change_event(
            self.disable_button_box(
                self.button_box_short,
                0,
                partial(self.int_a.check_linked_value, (None, 10)),
            )
        )

        self.function_button = els.FunctionButton(button_text="function", icon="Add", category=self.category_inputs)

        self.text_box = els.TextBox(label="Login", default_text="Hello", category=self.category_inputs)
        self.text_box_multi_line = els.TextBoxMultiLine(
            label="Example Multi Line",
            default_text="Hello\nmulti line",
            category=self.category_inputs,
        )
        self.text_box.deactivate_size_limit()
        self.pass_word = els.TextBox(
            label="Password",
            default_text="1234",
            category=self.category_inputs,
            password=True,
        )

        self.flex_option = els.FlexibleAmount(
            label=self.translations.flex_option,
            default_length=2,
            entry_mame="Layer",
            category=self.category_inputs,
            min_length=2,
            default_values=[["layer 1", 9.5, 3, 2], ["layer 2", 10.5, 2, 1]],
        )
        self.flex_option.add_option(els.TextBox, name="name", default_text="layer")

        self.flex_option.add_option(
            els.FloatBox,
            name="thickness",
            default_value=10,
            minimal_value=5,
            decimal_number=2,
        )
        self.flex_option.add_option(els.IntBox, name="amount", default_value=4, minimal_value=2)
        self.flex_option.add_option(
            els.ListBox,
            name="entry",
            default_index=0,
            entries=["entry 1", "entry 2", "entry 3"],
        )
        self.hint_flex = els.Hint(
            hint="wrong length of flexible option",
            category=self.category_inputs,
            warning=True,
        )
        self.flex_option.add_link_2_show(self.hint_flex, 2, 6)
        self.aim_plot.add_link_2_show(self.flex_option)
        # self.button_box.add_link_2_show(self.filename, on_index=1)
        self.show_option_under_multiple_conditions(
            self.filename,
            [self.button_box, self.aim_add],
            functions_check_for_and=[partial(self.button_box.check_linked_value, 1), self.aim_add.widget.isChecked],
        )

        self.category_grid = els.Category(page=self.page_inputs, label="Grid")
        self.category_grid.activate_grid_layout(3)
        self.hint_1 = els.Hint(category=self.category_grid, hint="Grid example")
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.int_small_1 = els.IntBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            category=self.category_grid,
        )
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.float_small_1 = els.FloatBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            decimal_number=2,
            category=self.category_grid,
        )
        self.hint_2 = els.Hint(category=self.category_grid, hint="Grid example")
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.int_small_2 = els.IntBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            category=self.category_grid,
        )
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.float_small_2 = els.FloatBox(
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
        self.numerical_results = els.Category(page=self.page_result, label="Numerical results")

        self.result_text_add = els.ResultText("Result", category=self.numerical_results, prefix="Result: ", suffix="m")
        self.result_text_add.text_to_be_shown("ResultsClass", "get_result")
        self.result_text_add.function_to_convert_to_text(lambda x: round(x, 2))
        self.result_depending_visibility = els.ResultText(
            "Result depending visibility", category=self.numerical_results, prefix="Result depending visibility: ", suffix="m"
        )
        self.result_depending_visibility.text_to_be_shown("ResultsClass", "get_result")
        self.result_depending_visibility.function_to_convert_to_text(lambda x: round(x, 2))
        self.result_text_sub = els.ResultText("Result", category=self.numerical_results, prefix="Result: ", suffix="m")
        self.result_text_sub.text_to_be_shown("ResultsClass", "result")
        self.result_text_sub.function_to_convert_to_text(lambda x: round(x, 2))

        # the option float_units is shown if int_small_2 is below 26 and (aim_plot is selected or int_small_1 is above 20)
        self.show_option_under_multiple_conditions(
            [self.result_depending_visibility, self.float_units],
            [self.aim_plot, self.int_small_1, self.int_small_2],
            custom_logic=lambda: (self.aim_plot.widget.isChecked() or self.int_small_1.check_linked_value((None, 20)))
            and self.int_small_2.check_linked_value((26, None)),
        )

        self.result_export = els.ResultExport(
            "Export results",
            icon="Download",
            category=self.numerical_results,
            export_function=ResultsClass.export,
            caption="Select file",
            file_extension="txt",
        )

        self.figure_results = els.ResultFigure(
            label=self.translations.figure_results,
            page=self.page_result,
            x_axes_text="X-Axes",
            y_axes_text="Y-Axes",
        )
        self.legend_figure_results = els.FigureOption(
            category=self.figure_results,
            label="Legend on",
            param="legend",
            default=0,
            entries=["No", "Yes"],
            entries_values=[False, True],
        )

        self.figure_results.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot")

        self.figure_results_multiple_lines = els.ResultFigure(
            label=self.translations.figure_results_multiple_lines,
            page=self.page_result,
            x_axes_text="X-Axes",
            y_axes_text="Y-Axes",
        )
        self.legend_figure_results_multiple_lines = els.FigureOption(
            category=self.figure_results_multiple_lines,
            label="Legend on",
            param="legend",
            default=0,
            entries=["No", "Yes"],
            entries_values=[False, True],
        )
        self.figure_results_multiple_lines.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot_multiple_lines")

        self.figure_results_with_different_other_saved_figure = els.ResultFigure(
            label=self.translations.figure_results, page=self.page_result, x_axes_text="X-Axes", y_axes_text="Y-Axes", customizable_figure=1
        )
        self.legend_figure_results_with_other_saved_figure = els.FigureOption(
            category=self.figure_results_with_different_other_saved_figure,
            label="Legend on",
            param="legend",
            default=0,
            entries=["No", "Yes"],
            entries_values=[False, True],
        )

        self.figure_results_with_different_other_saved_figure.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot")

        self.figure_results_with_customizable_layout = els.ResultFigure(
            label=self.translations.figure_results, page=self.page_result, x_axes_text="X-Axes", y_axes_text="Y-Axes", customizable_figure=2
        )
        self.legend_figure_results_with_customizable_layout = els.FigureOption(
            category=self.figure_results_with_customizable_layout,
            label="Legend on",
            param="legend",
            default=0,
            entries=["No", "Yes"],
            entries_values=[False, True],
        )

        self.figure_results_with_customizable_layout.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot")

        self.aim_add.add_link_2_show(self.result_text_add)
        self.aim_add.add_link_2_show(self.result_export)
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
        # you can either automatically links all pages by order of creation
        self.automatically_create_page_links()
        # or do this by hand like this:
        # self.page_inputs.set_next_page(self.page_result)
        # self.page_result.set_previous_page(self.page_inputs)
        # self.page_result.set_next_page(self.page_settings)
        # self.page_settings.set_previous_page(self.page_result)

    def check(self) -> bool:
        if self.started:
            logging.info("This should not be shown whilst loading")
