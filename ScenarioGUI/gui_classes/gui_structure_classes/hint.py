"""
hint class script
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs

from ...utils import change_font_size, set_default_font

if TYPE_CHECKING:  # pragma: no cover
    from .category import Category


class Hint:
    """
    This class contains all the functionalities of the Hint option in the GUI.
    Hints can be used to show text (for information or warnings) inside the category.
    """

    default_parent: QtW.QWidget | None = None

    def __init__(self, hint: str | list[str], category: Category, warning: bool = False):
        """

        Parameters
        ----------
        hint : List[str]
            Text of the hint
        category : Category
            Category in which the Hint should be placed
        warning : bool
            True if the Hint should be shown

        Examples
        --------
        >>> hint_example = Hint(hint="This is a hint to something important.",  # or self.translations.hint_example if hint_example is in Translation class
        >>>                     category=category_example,
        >>>                     warning=True)

        Gives:

        .. figure:: _static/Example_Hint.PNG

        """
        self.hint: list[str] = [hint] if isinstance(hint, str) else hint
        self.label: QtW.QLabel = QtW.QLabel(self.default_parent)
        self.warning = warning
        category.list_of_options.append(self)
        self.conditional_visibility: bool = False

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
        self.label.setParent(frame)
        self.label.setText(self.hint[0])
        if self.warning:
            self.label.setStyleSheet(f"color: {globs.WARNING};")
        set_default_font(self.label)
        self.label.setWordWrap(True)
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.label, column, row)
            return
        layout_parent.addWidget(self.label)

    def hide(self) -> None:
        """
        This function makes the Hint invisible.

        Returns
        -------
        None
        """
        self.label.hide()

    def show(self) -> None:
        """
        This function makes the current Hint visible.

        Returns
        -------
        None
        """
        self.label.show()

    def is_hidden(self) -> bool:
        """
        This function returns a boolean value related to whether or not the Hint is hidden.

        Returns
        -------
        Bool
            True if the option is hidden
        """
        return self.label.isHidden()

    def set_text(self, name: str):
        """
        This function sets the text of the Hint.

        Parameters
        ----------
        name : str
            Text of the Hint

        Returns
        -------
        None
        """
        self.label.setText(name)

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
        if self.label is not None:
            change_font_size(self.label, size, False)

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
        self.set_text(self.hint[idx])

    def __repr__(self):
        return f"{type(self).__name__}; Hint: {self.hint[0]}; Warning: {self.warning}"
