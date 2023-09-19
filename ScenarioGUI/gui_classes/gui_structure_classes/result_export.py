"""
function button class script
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ScenarioGUI.gui_classes.gui_structure_classes import FunctionButton

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    import PySide6.QtWidgets as QtW  # type: ignore

    from ..gui_structure_classes import Category


class ResultExport(FunctionButton):
    """
    This class contains all the functionalities of the FunctionButton option in the GUI.
    The FunctionButton can be used to couple a button press to a function call.
    """

    default_parent: QtW.QWidget | None = None

    def __init__(
        self,
        button_text: str | list[str],
        icon: str,
        *,
        category: Category,
        export_function: str | Callable[[str], None],
        file_extension: str = "",
        caption: str,
    ):
        """

        Parameters
        ----------
        button_text : list[str]
            The label of the FunctionButton
        icon : str
            Location of the icon for the FunctionButton
        category : Category
            Category in which the FunctionButton should be placed
        export_function : str, Callable
            export funciton nam
        file_extension : str
            file exentsion for export file
        caption : str
            caption of pop up window

        Examples
        --------
        >>> function_example = ResultExport(button_text="Press Here to activate function",
        >>> # or self.translations.function_example if function_example is in Translation class
        >>>                                   icon="example_icon.svg",
        >>>                                   category=category_example)  # type: ignore

        Gives:

        .. figure:: _static/Example_Function_Button.PNG

        """
        super().__init__(button_text, icon, category)
        self.file_extension: str = file_extension
        self.caption: str = caption
        self.export_function: str = export_function if isinstance(export_function, str) else export_function.__name__

    def set_text(self, name: str):
        """
        set text

        Parameters
        ----------
        name: str
            button text, caption separated by comma
        """
        names = name.split(",")
        super().set_text(names[0])
        if len(names) > 1:
            self.caption = names[1]

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
