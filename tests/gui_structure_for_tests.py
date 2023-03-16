from __future__ import annotations

from typing import TYPE_CHECKING

from ScenarioGUI.gui_classes.gui_structure import GuiStructure
from ScenarioGUI.gui_classes.gui_structure_classes import FloatBox, IntBox, Page, ResultText, Aim, Category

from examples.translation_class import Translations

if TYPE_CHECKING:
    import PySide6.QtWidgets as QtW


class GUI(GuiStructure):
    def __init__(self, default_parent: QtW.QWidget, translations: Translations):
        super().__init__(default_parent, translations)
        self.page_inputs = Page(name="Inputs", button_name="Inputs", icon="Add.svg")
        self.aim_add = Aim(label="Adding", icon="Add", page=self.page_inputs)
        self.aim_sub = Aim(label="Substract", icon="Delete", page=self.page_inputs)
        self.category_inputs = Category(page=self.page_inputs, label="Inputs")
        self.int_a = IntBox(
            label="a",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            category=self.category_inputs,
        )
        self.int_b = IntBox(
            label="b",
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
            category=self.category_inputs,
        )

        self.create_results_page()
        self.numerical_results = Category(
            page=self.page_result, label="Numerical results"
        )

        self.result_text_add = ResultText(
            "Result", category=self.numerical_results, prefix="Result: ", suffix="m"
        )
        self.result_text_add.text_to_be_shown("ResultsClass", "result")
        self.result_text_add.function_to_convert_to_text(lambda x: round(x, 2))
        self.result_text_sub = ResultText(
            "Result", category=self.numerical_results, prefix="Result: ", suffix="m"
        )
        self.result_text_sub.text_to_be_shown("ResultsClass", "result")
        self.result_text_sub.function_to_convert_to_text(lambda x: round(x, 2))
        self.aim_add.add_link_2_show(self.result_text_add)
        self.aim_sub.add_link_2_show(self.result_text_sub)

        self.create_settings_page()
        self.create_lists()