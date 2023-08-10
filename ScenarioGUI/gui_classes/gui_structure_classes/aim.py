"""
aim class script
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtGui as QtG  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs

from ...utils import change_font_size, set_default_font, Signal

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from .category import Category
    from .function_button import FunctionButton
    from .hint import Hint
    from .page import Page


    class Option(Protocol):
        label_text: str
        default_value: bool | int | float | str
        widget: QtW.QWidget | None
        frame: QtW.QFrame
        label: QtW.QLabel
        linked_options: list[(Option, int)]
        limit_size: bool
        list_2_check_before_value: list[tuple[Option, int], Aim]


class Aim:
    """
    This class contains all the functionalities of the Aim option in the GUI.
    The Aim option is central in the GHEtool GUI for it determines the possible 'things' one can do with the tool.
    """

    default_parent: QtW.QWidget | None = None

    def __init__(self, label: str | list[str], icon: str, page: Page):
        """

        Parameters
        ----------
        label : str | list[str]
            Names of the Aim for different languages
        icon : str
            Path to the icon for the Aim
        page : Page
            Page on which the Aim should be shown (normally, this is the first page)

        Examples
        --------
        >>> aim_example = Aim(label="Example aim",  # or self.translations.aim_example if aim_example is in Translation class
        >>>                   icon="example_icon.svg",
        >>>                   page=page_aim)

        Gives:

        .. figure:: _static/Example_Aim.PNG

        """
        self.label: list[str] = [label] if isinstance(label, str) else label
        self.icon: str = icon
        self.list_options: list[Option | Category | FunctionButton] = []
        self.visibilityChanged: Signal = Signal()
        self.valueChanged: Signal = Signal()
        self.widget: QtW.QPushButton = QtW.QPushButton(self.default_parent, toggled=self.valueChanged.emit)
        page.upper_frame.append(self)

    def show(self):
        self.widget.show()
        self.visibilityChanged.emit()

    def hide(self):
        self.widget.hide()
        self.visibilityChanged.emit()

    def is_hidden(self) -> bool:
        return self.widget.isHidden()

    def set_text(self, name: str) -> None:
        """
        This function sets the label text.

        Parameters
        ----------
        name : str
            Label name of the object

        Returns
        -------
        None
        """
        self.widget.setText(name)

    def set_font_size(self, size: int) -> None:
        """
        set the new font size to button

        Parameters
        ----------
        size: new font size in points

        Returns
        -------
            None
        """
        change_font_size(self.widget, size)

    def change_event(self, function_to_be_called: Callable, *, also_on_visibility: bool = False) -> None:
        """
        This function calls the function_to_be_called whenever the FloatBox is changed.

        Parameters
        ----------
        function_to_be_called : callable
            Function which should be called
        also_on_visibility: bool
            should the function also be called if the visibility has changed

        Returns
        -------
        None
        """
        self.valueChanged.connect(function_to_be_called)  # pylint: disable=E1101
        if also_on_visibility:
            self.visibilityChanged.connect(function_to_be_called)

    def add_link_2_show(self, option: Option | Category | FunctionButton | Hint):
        """
        This function couples the visibility of an option to the value of the Aim object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the FloatBox.

        Returns
        -------
        None

        Examples
        --------
        This function can be used to couple the Aim value to other options, hints, function buttons or categories.
        In the example below, 'option_example' will be shown if the Aim is selected.

        >>> aim_example.add_link_2_show(option=option_example)
        """
        self.list_options.append(option)

    def create_widget(self, frame: QtW.QFrame, layout: QtW.QGridLayout, idx: tuple[int, int]) -> None:
        """
        This functions creates the Aim widget in the grid layout.

        Parameters
        ----------
        frame : QtW.QFrame
            The frame object in which is the parent of the current widget
        layout : QtW.QGridLayout
            The grid layout in which the widget should be created
        idx : tuple[int, int]
            position in grid layout of the current Aim

        Returns
        -------
        None
        """
        icon11 = QtG.QIcon()
        icon11.addFile(f"{globs.FOLDER}/icons/{self.icon}")
        self.widget.setParent(frame)
        push_button = self.widget
        push_button.setIcon(icon11)
        push_button.setMinimumSize(QtC.QSize(0, 60))
        push_button.setMaximumSize(QtC.QSize(16777215, 60))
        push_button.setStyleSheet(
            f"QPushButton{'{'}border: 3px solid {globs.DARK};border-radius: 15px;color:{globs.WHITE};gridline-color: {globs.LIGHT};"
            f"background-color: {globs.GREY};{'}'}"
            f"QPushButton:hover{'{'}border: 3px solid {globs.DARK};background-color:{globs.LIGHT};{'}'}"
            f"QPushButton:checked{'{'}border:3px solid {globs.LIGHT};background-color:{globs.LIGHT};{'}'}\n"
            f"QPushButton:disabled{'{'}border: 3px solid {globs.GREY};border-radius: 5px;color: {globs.WHITE};gridline-color: {globs.GREY};"
            f"background-color: {globs.GREY};{'}'}\n"
            f"QPushButton:disabled:hover{'{'}background-color: {globs.DARK};{'}'}"
        )
        set_default_font(push_button, bold=True)
        push_button.setIconSize(QtC.QSize(30, 30))
        push_button.setCheckable(True)
        push_button.setText(self.label[0])
        layout.addWidget(push_button, idx[0], idx[1], 1, 1)

    def translate(self, idx: int) -> None:
        """
        Translates the label.

        Parameters
        ----------
        idx: int
            index of language

        Returns
        -------
        None
        """
        self.set_text(self.label[idx])
