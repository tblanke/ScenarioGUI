"""
This document contains all the information relevant for the GUI.
It contains all the options, categories etc. that should appear on the GUI.
"""
from typing import List, Tuple, Union

import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_structure_classes import (
    Aim,
    ButtonBox,
    Category,
    FunctionButton,
    Hint,
    ListBox,
    Option,
    Page,
    ResultFigure,
    ResultText,
)
from ScenarioGUI.gui_classes.translation_class import Translations


class GuiStructure:
    """
    This class contains all the elements that are relevant for the GUI.
    """

    def __init__(self, default_parent: QtW.QWidget, translations: Translations):
        """
        All the elements that should be placed on the GUI, should be written in
        chronologial order, in this __init__ function.
        """
        # set default parent for the class variables to avoid widgets creation not in the main window
        Page.default_parent = default_parent
        Aim.default_parent = default_parent
        Category.default_parent = default_parent
        Option.default_parent = default_parent
        Hint.default_parent = default_parent
        FunctionButton.default_parent = default_parent
        self.translations = translations

        # create page
        # self.page_result = None

        # self.cat_no_result = None
        # self.text_no_result = None

        # self.page_settings = None
        # self.category_language = None
        # self.option_language = None
        # self.category_save_scenario = None
        # self.option_toggle_buttons = None
        # self.option_auto_saving = None
        # self.hint_saving = None

        self.list_of_aims: List[Tuple[Aim, str]] = []
        self.list_of_options: List[Tuple[Option, str]] = []
        self.list_of_pages: List[Page] = []

        self.list_of_result_texts: List[Tuple[ResultText, str]] = []
        self.list_of_result_figures: List[Tuple[ResultFigure, str]] = []

        self.list_of_options_with_dependent_results: List[Tuple[Option, str]] = []

    def create_results_page(self):
        """
        creates the results page
        Returns
        -------
            None
        """
        self.page_result = Page("Results", "Results", "Result.svg")
        self.cat_no_result = Category(page=self.page_result, label="No results")
        self.text_no_result = Hint("No results are yet calculated", category=self.cat_no_result, warning=True)

    def create_settings_page(self):
        """
        creates the settings page
        Returns
        -------
            None
        """
        self.page_settings = Page("Settings", "Settings", "Settings.svg")

        self.category_language = Category(page=self.page_settings, label="Language")

        self.option_language = ListBox(
            category=self.category_language,
            label="Language: ",
            default_index=0,
            entries=[],
        )

        self.category_save_scenario = Category(page=self.page_settings, label="Scenario saving settings")

        self.option_toggle_buttons = ButtonBox(
            label="Toggle buttons?:",
            default_index=1,
            entries=[" no ", " yes "],
            category=self.category_save_scenario,
        )
        self.option_toggle_buttons.change_event(self.change_toggle_button)
        self.option_auto_saving = ButtonBox(
            label="Use automatic saving?:",
            default_index=0,
            entries=[" no ", " yes "],
            category=self.category_save_scenario,
        )
        self.hint_saving = Hint(
            category=self.category_save_scenario,
            hint="If Auto saving is selected the scenario will automatically saved if a scenario"
            " is changed. Otherwise the scenario has to be saved with the Update scenario "
            "button in the upper left corner if the changes should not be lost. ",
        )

    def create_lists(self):
        """
        creates the lists with the different elements
        """
        self.list_of_aims: List[Tuple[Aim, str]] = [(getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), Aim)]
        self.list_of_options: List[Tuple[Option, str]] = [(getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), Option)]
        self.list_of_pages: List[Page] = [getattr(self, name) for name in self.__dict__ if isinstance(getattr(self, name), Page)]

        self.list_of_result_texts: List[Tuple[ResultText, str]] = [
            (getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), ResultText)
        ]
        self.list_of_result_figures: List[Tuple[ResultFigure, str]] = [
            (getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), ResultFigure)
        ]

        self.list_of_options_with_dependent_results: List[Tuple[Option, str]] = [
            (getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), Option) if getattr(self, name).linked_options
        ]

    def change_toggle_button(self) -> None:
        """
        This function changes the behaviour of both the ButtonBox and aim selection
        from either toggle behaviour to not-change behaviour.

        Returns
        -------
        None
        """
        if self.option_toggle_buttons.get_value() == 0:
            ButtonBox.TOGGLE = False
            Page.TOGGLE = False
            return
        ButtonBox.TOGGLE = True
        Page.TOGGLE = True

    def translate(self, index: int, translation: Translations) -> None:
        """
        This function translates the GUI.

        Parameters
        ----------
        index : int
            Index of the language
        translation : Translations
            Class with all the translations

        Returns
        -------
        None
        """
        Page.next_label = translation.label_next[index]
        Page.previous_label = translation.label_previous[index]
        for name in [j for j in translation.__slots__ if hasattr(self, j)]:
            entry: Union[Option, Hint, FunctionButton, Page, Category] = getattr(self, name)
            entry.set_text(getattr(translation, name)[index])
