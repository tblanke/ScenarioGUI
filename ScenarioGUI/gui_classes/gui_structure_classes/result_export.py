"""
function button class script
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtGui as QtG  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs
from . import FunctionButton

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from ..gui_structure_classes import Category


class ResultExport(FunctionButton):
    """
    This class contains all the functionalities of the FunctionButton option in the GUI.
    The FunctionButton can be used to couple a button press to a function call.
    """

    default_parent: QtW.QWidget | None = None

    def __init__(self, button_text: str | list[str], icon: str, category: Category, export_function: str | Callable[[str]]):
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
        super().__init__(button_text, icon, category)
        self.FILE_EXTENSION: str = ".txt"
        self.caption: str = "Selecte file"
        self.export_function: str = export_function if isinstance(export_function, str) else export_function.__name__

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
