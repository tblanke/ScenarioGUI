"""
hint class script
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs
from . import Hint

from ...utils import change_font_size, set_default_font

if TYPE_CHECKING:  # pragma: no cover
    from .category import Category


class ValueHint(Hint):
    """
    This class contains all the functionalities of the Hint option in the GUI.
    Hints can be used to show text (for information or warnings) inside the category.
    """

    default_parent: QtW.QWidget | None = None

    def __init__(self, hint: str | list[str], category: Category, default_value: float = 0.0, warning: bool = False):
        """

        Parameters
        ----------
        hint : List[str]
            Text of the hint with a before text value and after text value split by ,
        category : Category
            Category in which the Hint should be placed
        warning : bool
            True if the Hint should be shown

        Examples
        --------
        >>> hint_example = ValueHint(hint="This is the temperature: , °C",  # or self.translations.hint_example if hint_example is in Translation class
        >>>                     category=category_example,
        >>>                     warning=True)

        Gives:

        .. figure:: _static/Example_Hint.PNG

        """
        super().__init__(hint, category, warning)
        self.label.setParent(None)
        self.frame: QtW.QFrame = QtW.QFrame(self.default_parent)
        self.label: list[QtW.QLabel] = [QtW.QLabel(self.default_parent), QtW.QLabel(self.default_parent), QtW.QLabel(self.default_parent)]
        self.default_value: float = default_value

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
        self.frame.setParent(frame)
        self.frame.setFrameShape(QtW.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtW.QFrame.Raised)
        self.frame.setStyleSheet("QFrame{\n" f" border: 0px solid {globs.WHITE};\n" f"	border-radius: 0px;\n{'}'}")
        layout_parent.addWidget(self.frame, column, row) if row is not None and isinstance(layout_parent, QtW.QGridLayout) else layout_parent.addWidget(self.frame)
        layout = QtW.QHBoxLayout(self.frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for label in self.label:
            label.setParent(self.frame)
            if self.warning:
                label.setStyleSheet(f"color: {globs.WARNING};")
            set_default_font(label)
            label.setWordWrap(False)
            layout.addWidget(label)

        spacer = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
        layout.addItem(spacer)

        self.set_text(self.hint[0])
        self.label[1].setText(f"{self.default_value:.2f}")

    def hide(self) -> None:
        """
        This function makes the Hint invisible.

        Returns
        -------
        None
        """
        self.frame.hide()

    def show(self) -> None:
        """
        This function makes the current Hint visible.

        Returns
        -------
        None
        """
        self.frame.show()

    def is_hidden(self) -> bool:
        """
        This function returns a boolean value related to whether or not the Hint is hidden.

        Returns
        -------
        Bool
            True if the option is hidden
        """
        return self.frame.isHidden()

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
        before_value, after_name = name.split(",")
        self.label[0].setText(before_value)
        self.label[2].setText(after_name)

    def set_text_value(self, value: float | str) -> None:
        """
        This function sets the text of the ResultText.
        This text is the combination of the prefix, the data (converted to string) and a suffix.

        Parameters
        ----------
        value: float | str
            value should be included into labels

        Returns
        -------
        None
        """
        self.label[1].setText(f"{value}")

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
        _ = [change_font_size(label, size, False) for label in self.label]

    def __repr__(self):
        return f"{type(self).__name__}; Hint: {self.label[0].text()}; Warning: {self.warning}"
