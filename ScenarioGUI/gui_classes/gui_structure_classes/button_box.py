"""
button box class script
"""
from __future__ import annotations

from functools import partial as ft_partial
from typing import TYPE_CHECKING

import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs

from .functions import check, update_opponent_not_change, update_opponent_toggle
from .option import Option

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from .category import Category
    from .function_button import FunctionButton
    from .hint import Hint


class ButtonBox(Option):
    """
    This class contains all the functionalities of the ButtonBox option in the GUI.
    The ButtonBox can be used to input floating point numbers.
    """

    TOGGLE: bool = True

    def __init__(self, label: str | list[str], default_index: int, entries: list[str], category: Category):
        """

        Parameters
        ----------
        label : str | List[str]
            The labels of the ButtonBox for different languages
        default_index : int
            The default index of the ButtonBox
        entries : List[str]
            The list of all the different buttons in the ButtonBox
        category : Category
            Category in which the ButtonBox should be placed

        Examples
        --------
        >>> option_buttons = ButtonBox(label="Button box label text",  # or self.translations.option_buttons if option_buttons is in Translation class
        >>>                            default_index=0,
        >>>                            entries=['option 1', 'option 2'],
        >>>                            category=category_example)

        Gives:

        .. figure:: _static/Example_Button_Box.PNG

        """
        super().__init__(label, default_index, category)
        self.entries: list[str] = entries
        self.widget: list[QtW.QPushButton] = [QtW.QPushButton(self.default_parent) for _ in self.entries]
        for idx, button in enumerate(self.widget):
            default_value = self.default_value if idx != self.default_value else idx - 1 if idx > 0 else 1
            button.clicked.connect(
                ft_partial(
                    self.update_function,
                    *(
                        button,
                        self.widget[default_value],
                        [but for but in self.widget if but not in [button, self.widget[default_value]]],
                    ),
                )
            )
            button.clicked.connect(ft_partial(check, self.linked_options, self, self.get_value()))

    def get_value(self) -> int:
        """
        This function gets the value of the ButtonBox.

        Returns
        -------
        int
            Value of the ButtonBox
        """
        for idx, button in enumerate(self.widget):
            if button.isChecked():
                return idx
        return -1

    def set_value(self, value: int) -> None:
        """
        This function sets the value of the ButtonBox.

        Parameters
        ----------
        value : int
            Value to which the ButtonBox should be set.

        Returns
        -------
        None
        """
        button = self.widget[value]
        if not button.isChecked():
            button.click()

    def _init_links(self) -> None:
        """
        Function on how the links for the ButtonBox should be set.

        Returns
        -------
        None
        """
        current_value: int = self.get_value()
        self.set_value(0 if current_value != 0 else 1)
        self.set_value(current_value)

    def _check_value(self) -> bool:
        """
        This function checks whether or not at least one button is checked.

        Returns
        -------
        bool
            True if at least one button is checked. False otherwise
        """
        return any(button.isChecked() for button in self.widget)

    def add_link_2_show(self, option: Option | Category | FunctionButton | Hint, on_index: int):
        """
        This function couples the visibility of an option to the value of the ButtonBox object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the FloatBox.
        on_index : int
            The index on which the linked options should be made visible.

        Returns
        -------
        None

        Examples
        --------
        This function can be used to couple the ButtonBox value to other options, hints, function buttons or categories.
        In the example below, 'option linked' will be shown if the first ('0') option is selected in the ButtonBox.

        >>> option_buttons.add_link_2_show(option=option_linked, on_index=0)
        """

        self.linked_options.append([option, on_index])

    def change_event(self, function_to_be_called: Callable) -> None:
        """
        This function calls the function_to_be_called whenever the ButtonBox is changed.

        Parameters
        ----------
        function_to_be_called : callable
            Function which should be called

        Returns
        -------
        None
        """
        for button in self.widget:
            button.clicked.connect(function_to_be_called)  # pylint: disable=E1101

    def set_text(self, name: str) -> None:
        """
        This function sets the text of the label and of the different buttons in the ButtonBox.

        Parameters
        ----------
        name: str
            String with the names of all the buttons (in order) and the label name at position 0.
            These strings are separated by ","

        Returns
        -------
        None
        """
        entry_name: list[str] = name.split(",")
        self.label.setText(entry_name[0])
        for button, button_name in zip(self.widget, entry_name[1:]):
            button.setText(f" {button_name.replace('++', ',')} ")

    def check_linked_value(self, value: int) -> bool:
        """
        This function checks if the linked "option" should be shown.

        Parameters
        ----------
        value : int
            int of index on which the option should be shown

        Returns
        -------
        bool
            True if the linked "option" should be shown
        """
        return self.get_value() == value

    def disable_entry(self, idx: int):
        """
        Disables the entry at index

        Parameters
        ----------
        idx: int
            index of entry which should be disabled
        """
        if self.widget[idx].isChecked():
            self.widget[idx].setChecked(False)
            self.widget[idx].setEnabled(False)
            if self.widget[self.default_value].isEnabled():
                self.widget[self.default_value].setChecked(True)
            else:
                widgets = [widget for widget in self.widget if widget.isEnabled()]
                if widgets:
                    widgets[0].setChecked(True)

        self.widget[idx].setEnabled(False)
        self.widget[idx].hide()
        if not [widget for widget in self.widget if widget.isEnabled()]:
            self.hide()
        #if len([widget for widget in self.widget if widget.isEnabled()]) == 1:
        #    [widget for widget in self.widget if widget.isEnabled()][0].setChecked(True)

    def enable_entry(self, idx: int):
        """
        Enables the entry at index

        Parameters
        ----------
        idx: int
            index of entry which should be disabled
        """
        self.show()
        self.widget[idx].setEnabled(True)
        self.widget[idx].show()
        if len([widget for widget in self.widget if widget.isEnabled()]) == 1:
            self.widget[idx].setChecked(True)

    def create_widget(
        self,
        frame: QtW.QFrame,
        layout_parent: QtW.QLayout,
        row: int = None,
        column: int = None,
    ) -> None:
        """
        This functions creates the ButtonBox widget in the frame.

        Parameters
        ----------
        frame : QtW.QFrame
            The frame object in which the widget should be created
        layout_parent : QtW.QLayout
            The parent layout of the current widget
        row : int
            The index of the row in which the widget should be created
            (only needed when there is a grid layout)
        column : int
            The index of the column in which the widget should be created
            (only needed when there is a grid layout)

        Returns
        -------
        None
        """
        layout = self.create_frame(frame, layout_parent)
        for idx, (entry, widget) in enumerate(zip(self.entries, self.widget)):
            widget.setParent(self.frame)
            widget.setText(f" {entry} ")
            widget.setStyleSheet(
                f"QPushButton{'{'}border: 3px solid {globs.DARK};border-radius: 5px;gridline-color: {globs.LIGHT};"
                f"background-color: {globs.GREY};font-weight:700;{'}'}"
                f"QPushButton:hover{'{'}border: 3px solid {globs.DARK};background-color:{globs.LIGHT};{'}'}"
                f"QPushButton:checked{'{'}border:3px solid {globs.LIGHT};background-color:{globs.LIGHT};{'}'}\n"
                f"QPushButton:disabled{'{'}border: 3px solid {globs.GREY};border-radius: 5px;color: {globs.WHITE};"
                f"gridline-color: {globs.GREY};background-color: {globs.GREY};{'}'}\n"
                f"QPushButton:disabled:hover{'{'}background-color: {globs.DARK};{'}'}"
            )
            widget.setCheckable(True)
            widget.setChecked(idx == self.default_value)
            widget.setMinimumHeight(30)
            font = widget.font()
            font.setFamily(globs.FONT)
            font.setPointSize(globs.FONT_SIZE)
            widget.setFont(font)
            layout.addWidget(widget)

    def update_function(
        self,
        button: QtW.QPushButton,
        button_opponent: QtW.QPushButton,
        false_button_list: list[QtW.QPushButton] = None,
    ) -> None:
        """
        This function updates which button should be checked/activated or unchecked/deactivated
        This can be done by either the toggle behaviour or not-change behaviour.

        Parameters
        ----------
        button : QtW.QPushButton
            Button which is activated (iff it was not already), and which is deactivated if it was active and is pressed on
        button_opponent : QtW.QPushButton
            Button which is activated if the current button was active and is pressed on
        false_button_list : List[QtW.QPushButton]
            List with other buttons which aren't active

        Returns
        -------
        None
        """
        if self.TOGGLE:
            update_opponent_toggle(button, button_opponent, false_button_list)
            return
        update_opponent_not_change(button, [*false_button_list, button_opponent])
