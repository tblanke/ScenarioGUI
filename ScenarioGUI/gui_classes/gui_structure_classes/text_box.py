"""
text box option class
"""
from __future__ import annotations

from functools import partial as ft_partial
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs

from ...utils import set_default_font
from .functions import check_conditional_visibility
from .option import Option

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from . import FunctionButton, Hint
    from .category import Category


class TextBox(Option):
    """
    This class contains all the functionalities of the TextBox option in the GUI.
    The TextBox can be used to input text.
    """

    def __init__(self, label: str | list[str], default_text: str, category: Category, *, password: bool = False, wrong_value: str = ""):
        """

        Parameters
        ----------
        label : str | list[str]
            The labels of the TextBox for differnt languages
        default_text : float
            The default value of the TextBox
        category : Category
            Category in which the FloatBox should be placed
        password : bool
            True if the TextBox should be a passowrd field with no visible letters
        wrong_value : str
            Value on which the textBox is wrong

        Examples
        --------
        >>> option_text = TextBox(label='Text label text',  # or self.translations.option_text if option_text is in Translation class
        >>>                       default_text="example text",
        >>>                       category=category_example)

        Gives:

        .. figure:: _static/Example_Text_Box.PNG

        """
        super().__init__(label, default_text, category)
        self.password: bool = password
        self.wrong_value: str = wrong_value
        self.widget: QtW.QLineEdit = QtW.QLineEdit(self.default_parent, textChanged=self.valueChanged.emit)

    def get_value(self) -> str:
        """
        This function gets the value of the TextBox.

        Returns
        -------
        str
            Value of the TextBox
        """
        return self.widget.text()

    def set_value(self, value: str) -> None:
        """
        This function sets the value of the TextBox.

        Parameters
        ----------
        value : str
            Value to which the TextBox should be set.

        Returns
        -------
        None
        """
        self.widget.setText(value)

    def _check_value(self) -> bool:
        """
        This function checks if the value of the FloatBox is between the minimal_value
        and maximal_value.

        Returns
        -------
        bool
            True if the value is between the minimal and maximal value
        """
        return self.get_value() != self.wrong_value

    def add_link_2_show(
        self,
        option: Option | Category | FunctionButton | Hint,
        value: str,
    ) -> None:
        """
        This function couples the visibility of an option to the value of the FloatBox object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the FloatBox.
        value : str
            string on which the option should be shown

        Returns
        -------
        None

        Examples
        --------
        This function can be used to couple the FloatBox value to other options, hints, function buttons or categories.
        In the example below, 'option linked' will be shown if the float value is below 0.1 or above 0.9.

        >>> option.add_link_2_show(option=option_linked, value="")
        """
        self.linked_options.append((option, value))
        check_conditional_visibility(option)

    def check_linked_value(self, value: str, value_if_hidden: bool | None = None) -> bool:
        """
        This function checks if the linked "option" should be shown.

        Parameters
        ----------
        value : str
            string on which the option should be shown
        value_if_hidden: bool | None
            the return value, if the option is hidden

        Returns
        -------
        bool
            True if the linked "option" should be shown
        """
        return self.check_value_if_hidden(self.get_value() == value, value_if_hidden)

    def create_function_2_check_linked_value(self, value: str, value_if_hidden: bool | None = None) -> Callable[[], bool]:
        """
        creates from values a function to check linked values

        Parameters
        ----------
        value : str
            string on which the option should be shown
        value_if_hidden: bool | None
            the return value, if the option is hidden

        Returns
        -------
        function
        """
        return ft_partial(self.check_linked_value, value, value_if_hidden)

    def create_widget(
        self,
        frame: QtW.QFrame,
        layout_parent: QtW.QLayout,
        row: int | None = None,
        column: int | None = None,
    ) -> None:
        """
        This functions creates the FloatBox widget in the frame.

        Parameters
        ----------
        frame : QtW.QFrame
            The frame object in which the widget should be created
        layout_parent : QtW.QLayout
            The parent layout of the current widget
        row : int | None
            The index of the row in which the widget should be created
            (only needed when there is a grid layout)
        column : int | None
            The index of the column in which the widget should be created
            (only needed when there is a grid layout)

        Returns
        -------
        None
        """
        layout = self.create_frame(frame, layout_parent)
        self.widget.setParent(self.frame)
        self.widget.setStyleSheet(
            f'QDoubleSpinBox{"{"}selection-color: {globs.WHITE};selection-background-color: {globs.LIGHT};'
            f'border: 1px solid {globs.WHITE};font: {globs.FONT_SIZE}pt "{globs.FONT}";{"}"}'
        )
        self.widget.setAlignment(QtC.Qt.AlignRight | QtC.Qt.AlignTrailing | QtC.Qt.AlignVCenter)
        self.widget.setProperty("showGroupSeparator", True)
        self.widget.setText(self.default_value)
        if self.password:
            self.widget.setEchoMode(QtW.QLineEdit.Password)
        if self.limit_size:
            self.widget.setMaximumWidth(150)
            self.widget.setMinimumWidth(150)
        self.widget.setMinimumHeight(28)
        set_default_font(self.widget)
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.widget, column, row)
            return
        layout.addWidget(self.widget)
