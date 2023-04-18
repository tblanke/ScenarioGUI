"""
This document contains all the information relevant for the GUI.
It contains all the options, categories etc. that should appear on the GUI.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ScenarioGUI import global_settings as globs
from ScenarioGUI.gui_classes.gui_structure_classes import (
    Aim,
    ButtonBox,
    Category,
    FunctionButton,
    Hint,
    IntBox,
    ListBox,
    Option,
    Page,
    ResultExport,
    ResultFigure,
    ResultText,
)

if TYPE_CHECKING:
    import PySide6.QtWidgets as QtW

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
        self.option_font_size = None

        self.list_of_aims: list[tuple[Aim, str]] = []
        self.list_of_options: list[tuple[Option, str]] = []
        self.list_of_pages: list[Page] = []
        self.list_of_rest: list[Hint | FunctionButton | Category] = []

        self.list_of_result_texts: list[tuple[ResultText, str]] = []
        self.list_of_result_figures: list[tuple[ResultFigure, str]] = []
        self.list_of_result_exports: list[tuple[ResultExport, str]] = []

        self.list_of_options_with_dependent_results: list[tuple[Option, str]] = []

    def create_results_page(self):
        """
        creates the results page
        Returns
        -------
            None
        """
        self.page_result = Page(self.translations.page_result, "Results", "Result.svg")
        self.cat_no_result = Category(page=self.page_result, label=self.translations.cat_no_results)
        self.text_no_result = Hint(self.translations.text_no_result, category=self.cat_no_result, warning=True)

    def create_settings_page(self):
        """
        creates the settings page
        Returns
        -------
            None
        """
        self.page_settings = Page(self.translations.page_settings, "Settings", "Settings.svg")

        self.category_language = Category(page=self.page_settings, label=self.translations.category_language)

        self.option_language = ListBox(
            category=self.category_language,
            label=self.translations.option_language,
            default_index=0,
            entries=[],
        )

        self.category_save_scenario = Category(page=self.page_settings, label=self.translations.category_save_scenario)

        self.option_toggle_buttons = ButtonBox(
            label=self.translations.option_toggle_buttons,
            default_index=1,
            entries=[" no ", " yes "],
            category=self.category_save_scenario,
        )
        self.option_toggle_buttons.change_event(self.change_toggle_button)
        self.option_n_threads = IntBox(label=self.translations.option_n_threads, default_value=2, category=self.category_save_scenario, minimal_value=1)
        self.option_font_size = IntBox(label=self.translations.option_font_size if hasattr(self.translations, "option_font_size") else "Font Size",
                                       default_value=globs.FONT_SIZE,
                                       category=self.category_save_scenario,
                                       minimal_value=8,
                                       maximal_value=20)
        self.option_auto_saving = ButtonBox(
            label=self.translations.option_auto_saving,
            default_index=0,
            entries=[" no ", " yes "],
            category=self.category_save_scenario,
        )
        self.hint_saving = Hint(
            category=self.category_save_scenario,
            hint=self.translations.hint_saving,
        )

    def create_lists(self):
        """
        creates the lists with the different elements
        """
        self.list_of_aims = [(getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), Aim)]
        self.list_of_options = [(getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), Option)]
        self.list_of_pages = [getattr(self, name) for name in self.__dict__ if isinstance(getattr(self, name), Page)]
        self.list_of_rest = [getattr(self, name) for name in self.__dict__ if isinstance(getattr(self, name), (Hint,
                                                                                                                                             FunctionButton,
                                                                                                                                            Category))]

        self.list_of_result_texts: list[tuple[ResultText, str]] = [
            (getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), ResultText)
        ]
        self.list_of_result_figures: list[tuple[ResultFigure, str]] = [
            (getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), ResultFigure)
        ]
        self.list_of_result_exports: list[tuple[ResultExport, str]] = [
            (getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), ResultExport)
        ]
        self.list_of_options_with_dependent_results: list[tuple[Option, str]] = [
            (getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), Option) if getattr(self, name).linked_options
        ]

    def change_font_size_2(self, size: int) -> None:
        """
        changes the font size to the size value

        Parameters
        ----------
        size: int
            new font size
        """
        _ = [option.set_font_size(size) for option, _ in self.list_of_options]
        _ = [aim.set_font_size(size) for aim, _ in self.list_of_aims]
        _ = [item.set_font_size(size) for item in self.list_of_rest]
        _ = [page.set_font_size(size) for page in self.list_of_pages]


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
            entry: Option | Hint | FunctionButton | Page | Category = getattr(self, name)
            try:
                entry.translate(index)
            except IndexError:
                logging.exception(name)
