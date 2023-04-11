"""
function button class script
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtGui as QtG  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs
from ...utils import change_font_size, set_default_font

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from ..gui_structure_classes import Category


class FunctionButton:
    """
    This class contains all the functionalities of the FunctionButton option in the GUI.
    The FunctionButton can be used to couple a button press to a function call.
    """

    default_parent: QtW.QWidget | None = None

    def __init__(self, button_text: str | list[str], icon: str, category: Category):
        """

        Parameters
        ----------
        button_text : list[str]
            The label of the FunctionButton
        icon : str
            Location of the icon for the FunctionButton
        category : Category
            Category in which the FunctionButton should be placed

        Examples
        --------
        >>> function_example = FunctionButton(button_text="Press Here to activate function",
        >>> # or self.translations.function_example if function_example is in Translation class
        >>>                                   icon=":/icons/icons/example_icon.svg",
        >>>                                   category=category_example)

        Gives:

        .. figure:: _static/Example_Function_Button.PNG

        """
        self.button_text: list[str] = [button_text] if isinstance(button_text, str) else button_text
        self.icon: str = icon
        self.frame: QtW.QFrame = QtW.QFrame(self.default_parent)
        self.button: QtW.QPushButton = QtW.QPushButton(self.default_parent)
        category.list_of_options.append(self)

    def create_widget(self, frame: QtW.QFrame, layout_parent: QtW.QLayout):
        """
        This functions creates the FunctionButton in the frame.

        Parameters
        ----------
        frame : QtW.QFrame
            The frame object in which the widget should be created
        layout_parent : QtW.QLayout
            The parent layout of the current widget

        Returns
        -------
        None
        """
        self.button.setParent(frame)
        self.button.setText(f"  {self.button_text[0]}  ")
        icon = QtG.QIcon()
        # icon11.addPixmap(QtGui_QPixmap(icon), QtGui_QIcon.Normal, QtGui_QIcon.Off)
        icon.addFile(f"{globs.FOLDER}/icons/{self.icon}")
        self.button.setIcon(icon)
        self.button.setIconSize(QtC.QSize(20, 20))
        self.button.setMinimumWidth(100)
        self.button.setMinimumHeight(35)
        set_default_font(self.button)
        self.frame.setParent(frame)
        self.frame.setFrameShape(QtW.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtW.QFrame.Raised)
        self.frame.setStyleSheet(f"QFrame{'{'}border: 0px solid {globs.WHITE};border-radius: 0px;{'}'}")
        layout = QtW.QHBoxLayout(self.frame)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        spacer1 = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
        layout.addItem(spacer1)

        layout.addWidget(self.button)
        spacer2 = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
        layout.addItem(spacer2)

        layout_parent.addWidget(self.frame)

    def hide(self) -> None:
        """
        This function makes the FunctionButton invisible.

        Returns
        -------
        None
        """
        self.frame.hide()

    def show(self) -> None:
        """
        This function makes the current FunctionButton visible.

        Returns
        -------
        None
        """
        self.frame.show()

    def is_hidden(self) -> bool:
        """
        This function returns a boolean value related to whether or not the FunctionButton is hidden.

        Returns
        -------
        Bool
            True if the option is hidden
        """
        return self.frame.isHidden()

    def set_text(self, name: str):
        """
        This function sets the text of the FunctionButton.

        Parameters
        ----------
        name : str
            Text of the FunctionButton

        Returns
        -------
        None
        """
        self.button.setText(name)

    def change_event(self, function_to_be_called: Callable, *args) -> None:
        """
        This function calls the function_to_be_called whenever the FunctionButton is pressed.

        Parameters
        ----------
        function_to_be_called : callable
            Function which should be called
        args
            Arguments to be passed through to the function_to_be_called

        Returns
        -------
        None
        """
        self.button.clicked.connect(lambda: function_to_be_called(*args))

    def set_font_size(self, size: int) -> None:
        """
        set the text size of hint

        Parameters
        ----------
        size: int
            new font size as points
        Returns
        -------

        """
        if self.button is not None:
            change_font_size(self.button, size, False)

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
        self.set_text(self.button_text[idx])
