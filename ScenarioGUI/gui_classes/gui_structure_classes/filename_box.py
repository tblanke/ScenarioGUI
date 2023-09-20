"""
filename box
"""
from __future__ import annotations

import logging
from functools import partial
from os.path import exists
from pathlib import Path
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs

from ...utils import change_font_size, set_default_font
from .functions import check_conditional_visibility
from .option import Option

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from . import FunctionButton, Hint
    from .category import Category


class FileNameBox(Option):
    """
    This class contains all the functionalities of the FileNameBox (filename input box) option in the GUI.
    The FileNameBox can be used to import a datafile.
    """

    def __init__(
        self,
        label: str | list[str],
        default_value: str,
        category: Category,
        *,
        dialog_text: str = "",
        error_text: str = "",
        file_extension: str | list[str] = "csv",
    ):
        """

        Parameters
        ----------
        label : str | list[str]
            The labels of the FileNameBox for different languages
        default_value : int
            The default value of the FileNameBox
        category : Category
            Category in which the FileNameBox should be placed
        dialog_text : str
            Text to be displayed in the top bar of the dialog box
        error_text : str
            Error text to be shown in the status_bar

        Examples
        --------
        >>> option_file = FileNameBox(label="File name box label text",  # or self.translations.option_file if option_file is in Translation class
        >>>                           default_value='example_file.XX',
        >>>                           dialog_text='Choose *.XX file',
        >>>                           error_text='no file found',
        >>>                           file_extension="csv",
        >>>                           category=category_example)

        Gives:

        .. figure:: _static/Example_Filename.PNG

        """
        super().__init__(label, default_value, category)
        self.widget: QtW.QLineEdit = QtW.QLineEdit(self.default_parent)
        self.dialog_text: str = dialog_text
        self.error_text: str = error_text
        self.button: QtW.QPushButton = QtW.QPushButton(self.default_parent)
        self.file_extension = [file_extension] if isinstance(file_extension, str) else file_extension
        self.check_active: bool = False
        self.widget.textChanged.connect(self.valueChanged.emit)

    def get_value(self) -> str:
        """
        This function returns the filename (with path) which is put into the FileNameBox.

        Returns
        -------
        str
            Filename (with path)
        """
        return self.widget.text()

    def set_value(self, value: str) -> None:
        """
        This function sets the value of the FileNameBox.

        Parameters
        ----------
        value : int
            Value to which the FileNameBox should be set.

        Returns
        -------
        None
        """
        self.widget.setText(value)

    def _check_value(self) -> bool:
        """
        This function checks whether a value is given in the FileNameBox.

        Returns
        -------
        bool
            True if a value is given in the FileNameBox. False otherwise
        """
        return exists(self.widget.text()) if self.check_active else True

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
        return partial(self.check_linked_value, value, value_if_hidden)

    def create_widget(
        self,
        frame: QtW.QFrame,
        layout_parent: QtW.QLayout,
        row: int | None = None,
        column: int | None = None,
    ) -> None:
        """
        This functions creates the ButtonBox widget in the frame.

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
        layout = self.create_frame(frame, layout_parent, False)
        self.widget.setParent(self.frame)
        self.widget.setStyleSheet(
            f"QLineEdit{'{'}border: 3px solid {globs.LIGHT};border-radius: 5px;color: {globs.WHITE};gridline-color: {globs.LIGHT};"
            f"background-color: {globs.LIGHT};\n"
            f"selection-background-color: {globs.LIGHT_SELECT};{'}'}\n"
            f"QLineEdit:hover{'{'}background-color: {globs.DARK};{'}'}"
        )
        self.widget.setText(self.default_value)
        set_default_font(self.widget)
        layout.addWidget(self.widget)
        self.button.setParent(self.frame)
        self.button.setMinimumSize(QtC.QSize(30, 30))
        self.button.setMaximumSize(QtC.QSize(30, 30))
        self.button.setText("...")
        set_default_font(self.button)
        self.button.clicked.connect(self.fun_choose_file)  # pylint: disable=E1101
        layout.addWidget(self.button)

    def set_font_size(self, size: int) -> None:
        """
        set the new font size to label, text box and button

        Parameters
        ----------
        size: new font size in points

        Returns
        -------
            None
        """
        super().set_font_size(size)
        change_font_size(self.button, size)

    def fun_choose_file(self) -> None:
        """
        This function opens a file selector, with which the filename path can be selected.
        This is automatically added to the FileNameBox.

        Returns
        -------
        None
        """
        # try to ask for a file otherwise show message in status bar
        file_extensions = [f".{extension} (*.{extension})" for extension in self.file_extension]
        file_extensions = ";;".join(file_extensions)
        filename = QtW.QFileDialog.getOpenFileName(self.frame, caption=self.dialog_text, filter=file_extensions, dir=str(Path.home()))
        if not filename[0]:
            logging.error(self.error_text)
            return
        self.set_value(filename[0])
