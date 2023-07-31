"""
text box multi line option class
"""
from __future__ import annotations

from functools import partial as ft_partial
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs

from ...utils import set_default_font
from .option import Option

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from .category import Category


class TextBoxMultiLine(Option):
    """
    This class contains all the functionalities of the TextBoxMultiLine option in the GUI.
    The TextBoxMultiMine can be used to input text across multiple lines.
    """
    def __init__(
        self,
        label: str | list[str],
        default_text: str,
        category: Category,
        *,
        wrong_value: str = ""
    ):
        """

        Parameters
        ----------
        label : str | list[str]
            The labels of the TextBox for differnt languages
        default_text : float
            The default value of the TextBox
        category : Category
            Category in which the FloatBox should be placed
        wrong_value : str
            Value on which the textBox is wrong

        Examples
        --------
        >>> option_text = TextBoxMultiLine(label='Example Multiple Line',  # or self.translations.option_text if option_text is in Translation class
        >>>                       default_text='Hello multi line',
        >>>                       category=category_example)

        Gives:

        .. figure:: _static/Example_mulitple_line_text.PNG

        """
        super().__init__(label, default_text, category)
        self.wrong_value: str = wrong_value
        self.widget: QtW.QTextEdit = QtW.QTextEdit(self.default_parent)

    def get_value(self) -> str:
        """
        This function gets the value of the TextBox.

        Returns
        -------
        str
            Value of the TextBox
        """
        return self.widget.toPlainText()

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

    def _init_links(self) -> None:
        """
        Function on how the links for the FloatBox should be set.

        Returns
        -------
        None
        """
        current_value: str = self.get_value()
        self.set_value(f"{current_value}1")
        self.set_value(current_value)

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

    def check_linked_value(self, value: str) -> bool:
        """
        This function checks if the linked "option" should be shown.

        Parameters
        ----------
        value : str
            str on which the option should be shown

        Returns
        -------
        bool
            True if the linked "option" should be shown
        """
        return self.get_value() == value

    def create_function_2_check_linked_value(self, value: str, value_if_hidden: bool | None) -> Callable[[], bool]:
        """
        creates from values a function to check linked values

        Parameters
        ----------
        value : str
            str on which the option should be shown
        value_if_hidden: bool
            the return value, if the option is hidden

        Returns
        -------
        function
        """
        if value_if_hidden is None:
            return ft_partial(self.check_linked_value, value)

        def func():
            if self.is_hidden():
                return value_if_hidden
            self.check_linked_value(value)

        return func

    def change_event(self, function_to_be_called: Callable) -> None:
        """
        This function calls the function_to_be_called whenever the FloatBox is changed.

        Parameters
        ----------
        function_to_be_called : callable
            Function which should be called

        Returns
        -------
        None
        """
        self.widget.textChanged.connect(function_to_be_called)  # pylint: disable=E1101

    def create_widget(
        self,
        frame: QtW.QFrame,
        layout_parent: QtW.QLayout,
        row: int = None,
        column: int = None,
    ) -> None:
        """
        This functions creates the FloatBox widget in the frame.

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
        self.widget.setParent(self.frame)
        self.widget.setStyleSheet(
            f"QTextEdit{'{'}border: 3px solid {globs.LIGHT};border-radius: 5px;color: {globs.WHITE};gridline-color: {globs.LIGHT};background-color: {globs.LIGHT};font-weight:500;\n"
            f"selection-background-color: {globs.LIGHT_SELECT};{'}'}\n"
            f"QTextEdit:hover{'{'}background-color: {globs.DARK};{'}'}"
        )
        self.widget.setAlignment(QtC.Qt.AlignmentFlag.AlignRight)
        self.widget.setProperty("showGroupSeparator", True)
        self.widget.setText(self.default_value)
        if self.limit_size:
            self.widget.setMaximumWidth(500)
            self.widget.setMinimumWidth(150)
        self.widget.setMinimumHeight(60)
        set_default_font(self.widget)
        # self.widget.setMaximumSize(QtC.QSize(500, 90))
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.widget, column, row)
            return
        layout.addWidget(self.widget)
