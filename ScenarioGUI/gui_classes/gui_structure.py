"""
This document contains all the information relevant for the GUI.
It contains all the options, categories etc. that should appear on the GUI.
"""
from __future__ import annotations

from functools import partial
from typing import Protocol, TYPE_CHECKING

import numpy as np

from ScenarioGUI import global_settings as globs
from ScenarioGUI.gui_classes.gui_structure_classes import (
    Aim,
    ButtonBox,
    Category,
    FigureOption,
    FlexibleAmount,
    FloatBox,
    FunctionButton,
    Hint,
    IntBox,
    ListBox,
    MultipleIntBox,
    Option,
    Page,
    ResultExport,
    ResultFigure,
    ResultText,
)
from ScenarioGUI.gui_classes.gui_structure_classes.font_list_box import FontListBox
from ScenarioGUI.gui_classes.gui_structure_classes.functions import check_conditional_visibility
from ScenarioGUI.gui_classes.gui_structure_classes.result_figure import font_list, get_name

if TYPE_CHECKING:
    from collections.abc import Callable

    import PySide6.QtWidgets as QtW

    from ScenarioGUI.gui_classes.translation_class import Translations


    class OptionShow(Protocol):

        def show(self):
            """"""

        def hide(self):
            """"""



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

        # flag for loading the gui
        self.started: bool = False
        # flag for loading a file
        self.loaded: bool = False

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
        self.cat_no_results = Category(page=self.page_result, label=self.translations.cat_no_results)
        self.text_no_result = Hint(self.translations.text_no_result, category=self.cat_no_results, warning=True)

    def automatically_create_page_links(self):
        # couple to previous and next buttons
        _ = [page.set_previous_page(page_previous) for page, page_previous in zip(self.list_of_pages[1:], self.list_of_pages[:-1])]
        _ = [page.set_next_page(page_next) for page, page_next in zip(self.list_of_pages[:-1], self.list_of_pages[1:])]

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
        self.option_n_threads = IntBox(
            label=self.translations.option_n_threads,
            default_value=2,
            category=self.category_save_scenario,
            minimal_value=1,
        )
        self.time_out = FloatBox(label=self.translations.time_out if hasattr(self.translations, "time_out") else "Maximal runtime [s]:", default_value=600,
                                 category=self.category_save_scenario, minimal_value=1, maximal_value=3600*24)
        self.option_font_size = IntBox(
            label=self.translations.option_font_size if hasattr(self.translations, "option_font_size") else "Font size",
            default_value=globs.FONT_SIZE,
            category=self.category_save_scenario,
            minimal_value=8,
            maximal_value=20,
        )
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

        self.category_default_figure_settings = Category(
            label=self.translations.category_default_figure_settings
            if hasattr(self.translations, "category_default_figure_settings")
            else "Default figure settings",
            page=self.page_settings,
        )

        self.option_figure_background = MultipleIntBox(
            label=self.translations.option_figure_background
            if hasattr(self.translations, "option_figure_background")
            else "Figure background color in rgb code?",
            default_value=np.array(
                globs.DARK.replace("rgb(", "").replace(")", "").split("," ""),
                dtype=np.float64,
            ),
            category=self.category_default_figure_settings,
            minimal_value=0,
            maximal_value=255,
            step=1,
        )
        self.option_plot_background = MultipleIntBox(
            label=self.translations.option_plot_background if hasattr(self.translations, "option_plot_background") else "Plot background color in rgb code?",
            default_value=np.array(
                globs.WHITE.replace("rgb(", "").replace(")", "").split("," ""),
                dtype=np.float64,
            ),
            category=self.category_default_figure_settings,
            minimal_value=0,
            maximal_value=255,
            step=1,
        )
        self.option_axes_text = MultipleIntBox(
            label=self.translations.option_axes_text if hasattr(self.translations, "option_axes_text") else "Axes text color in rgb code?",
            default_value=np.array(
                globs.WHITE.replace("rgb(", "").replace(")", "").split("," ""),
                dtype=np.float64,
            ),
            category=self.category_default_figure_settings,
            minimal_value=0,
            maximal_value=255,
            step=1,
        )
        self.option_axes = MultipleIntBox(
            label=self.translations.option_axes if hasattr(self.translations, "option_axes") else "Axes color in rgb code?",
            default_value=np.array(
                globs.WHITE.replace("rgb(", "").replace(")", "").split("," ""),
                dtype=np.float64,
            ),
            category=self.category_default_figure_settings,
            minimal_value=0,
            maximal_value=255,
            step=1,
        )
        self.option_title = MultipleIntBox(
            label=self.translations.option_title if hasattr(self.translations, "option_title") else "Title color in rgb code?",
            default_value=np.array(
                globs.WHITE.replace("rgb(", "").replace(")", "").split("," ""),
                dtype=np.float64,
            ),
            category=self.category_default_figure_settings,
            minimal_value=0,
            maximal_value=255,
            step=1,
        )
        self.option_legend_text = MultipleIntBox(
            label=self.translations.option_legend_text if hasattr(self.translations, "option_legend_text") else "Legend text color in rgb code?",
            default_value=np.array(
                globs.DARK.replace("rgb(", "").replace(")", "").split("," ""),
                dtype=np.float64,
            ),
            category=self.category_default_figure_settings,
            minimal_value=0,
            maximal_value=255,
            step=1,
        )
        self.option_font_size_figure = IntBox(
            label=self.translations.option_font_size if hasattr(self.translations, "option_font_size") else "Font Size:",
            default_value=globs.FONT_SIZE,
            minimal_value=6,
            maximal_value=40,
            category=self.category_default_figure_settings,
        )
        self.option_font = FontListBox(
            label=self.translations.option_font if hasattr(self.translations, "option_font") else "Font family: ",
            category=self.category_default_figure_settings,
            entries=[get_name(font) for font in font_list],
            default_index=[get_name(font).upper() for font in font_list].index(globs.FONT.upper()),
        )
        self.option_figure_background.change_event(self.change_figure_background_color)
        self.option_plot_background.change_event(self.change_plot_background_color)
        self.option_axes_text.change_event(self.change_axes_text)
        self.option_axes.change_event(self.change_axes)
        self.option_font.change_event(self.change_font)
        self.option_font_size_figure.change_event(self.change_font_size)
        self.option_legend_text.change_event(self.change_legend_color)
        self.option_title.change_event(self.change_title)

    def set_figure_translations(self):
        for fig, _ in self.list_of_result_figures:
            if not fig.customizable_figure == 2:
                continue
            for option, name in zip(
                [
                    fig.option_axes,
                    fig.option_font,
                    fig.option_font_size,
                    fig.option_title,
                    fig.option_title,
                    fig.option_legend_text,
                    fig.option_plot_background,
                    fig.option_figure_background,
                    fig.default_figure_colors,
                ],
                [
                    "option_axes",
                    "option_font",
                    "option_font_size",
                    "option_title",
                    "option_title",
                    "option_legend_text",
                    "option_plot_background",
                    "option_figure_background",
                    "default_figure_colors",
                ],
            ):
                option.label_text = getattr(self.translations, name) if hasattr(self.translations, name) else option.label_text
            fig.option_save_layout.button_text = (
                self.translations.option_save_layout if hasattr(self.translations, "option_save_layout") else fig.option_save_layout.button_text
            )

    def create_lists(self):
        """
        creates the lists with the different elements
        """
        self.list_of_aims = [(getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), Aim)]
        self.list_of_options = [(getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), Option)]
        self.list_of_pages = [getattr(self, name) for name in self.__dict__ if isinstance(getattr(self, name), Page)]
        self.list_of_rest = [getattr(self, name) for name in self.__dict__ if isinstance(getattr(self, name), (Hint, FunctionButton, Category))]

        self.list_of_result_texts: list[tuple[ResultText, str]] = [
            (option, "") for cat in self.page_result.list_categories for option in cat.list_of_options if isinstance(option, ResultText)
        ]

        self.list_of_result_figures: list[tuple[ResultFigure, str]] = [
            (getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), ResultFigure)
        ]
        self.category_default_figure_settings.hide() if not self.list_of_result_figures else self.category_default_figure_settings.show()
        for fig in [fig for fig, _ in self.list_of_result_figures if fig.customizable_figure == 2]:  # noqa: PLR2004
            fig.option_save_layout.change_event(
                partial(
                    self.save_layout_from_figure,
                    fig.option_figure_background,
                    fig.option_plot_background,
                    fig.option_axes_text,
                    fig.option_axes,
                    fig.option_font,
                    fig.option_font_size,
                    fig.option_legend_text,
                    fig.option_title,
                )
            )
        self.list_of_result_exports: list[tuple[ResultExport, str]] = [
            (getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), ResultExport)
        ]
        self.list_of_options_with_dependent_results: list[tuple[Option, str]] = [
            (getattr(self, name), name) for name in self.__dict__ if isinstance(getattr(self, name), Option) if getattr(self, name).linked_options
        ]
        self.set_figure_translations()

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

    def change_figure_background_color(self):
        for fig, _ in self.list_of_result_figures:
            if not fig.customizable_figure == 2:
                continue
            fig.option_figure_background.set_value(self.option_figure_background.get_value())
            fig.update_default_settings()

    def change_plot_background_color(self):
        for fig, _ in self.list_of_result_figures:
            if not fig.customizable_figure == 2:
                continue
            fig.option_plot_background.set_value(self.option_plot_background.get_value())
            fig.update_default_settings()

    def change_font_size(self):
        for fig, _ in self.list_of_result_figures:
            if not fig.customizable_figure == 2:
                continue
            fig.option_font_size.set_value(self.option_font_size_figure.get_value())
            fig.update_default_settings()

    def change_font(self):
        for fig, _ in self.list_of_result_figures:
            if not fig.customizable_figure == 2:
                continue
            fig.option_font.set_value(self.option_font.get_value())
            fig.update_default_settings()

    def change_legend_color(self):
        for fig, _ in self.list_of_result_figures:
            if not fig.customizable_figure == 2:
                continue
            fig.option_legend_text.set_value(self.option_legend_text.get_value())
            fig.update_default_settings()

    def change_axes(self):
        for fig, _ in self.list_of_result_figures:
            if not fig.customizable_figure == 2:
                continue
            fig.option_axes.set_value(self.option_axes.get_value())
            fig.update_default_settings()

    def change_axes_text(self):
        for fig, _ in self.list_of_result_figures:
            if not fig.customizable_figure == 2:
                continue
            fig.option_axes_text.set_value(self.option_axes_text.get_value())
            fig.update_default_settings()

    def change_title(self):
        for fig, _ in self.list_of_result_figures:
            if not fig.customizable_figure == 2:
                continue
            fig.option_title.set_value(self.option_title.get_value())
            fig.update_default_settings()

    def save_layout_from_figure(
        self,
        option_figure_background: MultipleIntBox,
        option_plot_background: MultipleIntBox,
        option_axes_text: MultipleIntBox,
        option_axes: MultipleIntBox,
        option_font: FontListBox,
        option_font_size_figure: IntBox,
        option_legend_text: MultipleIntBox,
        option_title: MultipleIntBox,
    ):
        self.option_figure_background.set_value(option_figure_background.get_value())
        self.option_plot_background.set_value(option_plot_background.get_value())
        self.option_axes_text.set_value(option_axes_text.get_value())
        self.option_axes.set_value(option_axes.get_value())
        self.option_font.set_value(option_font.get_value())
        self.option_font_size_figure.set_value(option_font_size_figure.get_value())
        self.option_legend_text.set_value(option_legend_text.get_value())
        self.option_title.set_value(option_title.get_value())

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

    def disable_button_box(self, button_box: ButtonBox, at_index: int, func_2_check: Callable[[], bool]) -> Callable[[]]:
        return partial(self._disable_button_box, button_box, at_index, func_2_check)

    @staticmethod
    def _disable_button_box(button_box: ButtonBox, at_index: int, func_2_check: Callable[[], bool], *args):
        if func_2_check():
            button_box.disable_entry(at_index)
            # emit valueChanged signal
            button_box.valueChanged.emit()
            return
        button_box.enable_entry(at_index)

    def disable_aim(self, aim: Aim, at_page: Page, func_2_check: Callable[[], bool]) -> Callable[[]]:
        return partial(self._disable_aim, aim, at_page, func_2_check)

    @staticmethod
    def _disable_aim(aim: Aim, at_page: Page, func_2_check: Callable[[], bool], *args):
        if func_2_check():
            if aim.is_checked():
                aim.widget.click()
            aim.widget.setEnabled(False)
            font = aim.widget.font()
            font.setStrikeOut(True)
            aim.widget.setFont(font)
            if aim.is_checked():
                # if toggled is not enabled, the button is still checked
                aim.widget.setChecked(False)
                aims = [aim_i for aim_i in at_page.upper_frame if aim_i != aim and aim_i.widget.isEnabled()]
                if aims:
                    aims[0].widget.setChecked(True)
            return
        aim.widget.setEnabled(True)
        font = aim.widget.font()
        font.setStrikeOut(False)
        aim.widget.setFont(font)
        if len([aim_i for aim_i in at_page.upper_frame if aim_i.widget.isEnabled()]) == 1:
            aim.widget.setChecked(True)

    @staticmethod
    def show_option_under_multiple_conditions(options_to_be_shown: OptionShow | list[OptionShow],  # noqa: PLR0913
                                              options_2_be_checked: Option | Aim | list[Option | Aim], *,
                                              functions_check_for_and: list[Callable[[], bool]] | None = None,
                                              functions_check_for_or: list[Callable[[], bool]] | None = None,
                                              custom_logic: Callable[[], bool] | None = None,
                                              check_on_visibility_change: bool = False) -> None:
        """
        show the option_to_be_shown if all functions_of_options of the options_2_be_checked are returning true\n
        Important!: This function can only be used once per option. Otherwise, this can lead to unexpected behaviour, where most probably the last function
        call is the dominant one.

        Parameters
        ----------
        options_to_be_shown: Option or list of options
            The option (or list of options) which should be shown if all conditions are met
        options_2_be_checked: list[Option]
            list of options and function of the options that evoke the evaluation of the logical values
        functions_check_for_and: list[Callable[[], bool]] | None
            list of options and function of the options that should be checked for the "and" condition (so all have to be true)
        functions_check_for_or: list[Callable[[], bool]] | None
            list of options and function of the options that should be checked for the "or" condition (so one have to be true)
        custom_logic : Callable
            custom logic for the evaluation of the truth value
        check_on_visibility_change: bool
            check also on visibility change

        Returns
        -------
            None
        """

        options_to_be_shown: list[Option] = [options_to_be_shown] if not isinstance(options_to_be_shown, list) else options_to_be_shown

        options_2_be_checked = [options_2_be_checked] if not isinstance(options_2_be_checked, list) else options_2_be_checked

        # check if conditional visibility is already assigned
        [check_conditional_visibility(option) for option in options_2_be_checked]

        if np.sum([functions_check_for_and is not None, functions_check_for_or is not None, custom_logic is not None]) > 1:
            raise UserWarning('Multiple criteria for the truth evaluation are selected. Please choose either the and, or or custom logic criterium.')

        if functions_check_for_and is not None:
            def check():
                _ = [i.show() for i in options_to_be_shown] if all(func() for func in functions_check_for_and) else [i.hide() for i in options_to_be_shown]
        elif functions_check_for_or:
            def check():
                _ = [i.show() for i in options_to_be_shown] if any(func() for func in functions_check_for_or) else [i.hide() for i in options_to_be_shown]
        else:
            def check():
                _ = [i.show() for i in options_to_be_shown] if custom_logic() else [i.hide() for i in options_to_be_shown]
        for option in options_2_be_checked:
            option.change_event(check, also_on_visibility=check_on_visibility_change)

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
        _ = [option.translate(index) for option, _ in self.list_of_options if len(option.label_text) > index and len(option.label_text) > 1]
        _ = [aim.translate(index) for aim, _ in self.list_of_aims if len(aim.label) > index and len(aim.label) > 1]
        _ = [page.translate(index) for page in self.list_of_pages if len(page.name) > index and len(page.name) > 1]
        for fig, _ in self.list_of_result_figures:
            if not fig.customizable_figure == 2:
                continue
            for option in [
                fig.option_axes,
                fig.option_font,
                fig.option_font_size,
                fig.option_title,
                fig.option_title,
                fig.option_legend_text,
                fig.option_plot_background,
                fig.option_figure_background,
                fig.default_figure_colors,
            ]:
                option.translate(index) if len(option.label_text) > index and len(option.label_text) > 1 else None
            fig.option_save_layout.translate(index) if len(fig.option_save_layout.button_text) > index and len(fig.option_save_layout.button_text) > 1 else None
        for item in self.list_of_rest:
            if isinstance(item, Hint) and len(item.hint) > index and len(item.hint) > 1:
                item.translate(index)
            if isinstance(item, FunctionButton) and len(item.button_text) > index and len(item.button_text) > 1:
                item.translate(index)
            if isinstance(item, Category) and len(item.label_text) > index and len(item.label_text) > 1:
                item.translate(index)
