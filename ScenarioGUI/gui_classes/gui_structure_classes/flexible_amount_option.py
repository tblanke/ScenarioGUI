"""
float box option class
"""
from __future__ import annotations

from enum import Enum, auto
from functools import partial as ft_partial
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs

from .option import Option
from copy import deepcopy

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from .category import Category
    from .function_button import FunctionButton
    from .hint import Hint


class FlexibleAmount(Option):
    """
    This class contains all the functionalities of the FloatBox option in the GUI.
    The FloatBox can be used to input floating point numbers.
    """

    def __init__(
        self,
        label: str,
        entry_mame: str,
        category: Category,
    ):
        """

        Parameters
        ----------
        label : str
            The label of the FloatBox
        category : Category
            Category in which the FloatBox should be placed

        Examples
        --------
        >>> option_float = FloatBox(label='Float label text',
        >>>                         default_value=0.5,
        >>>                         category=category_example,
        >>>                         decimal_number=2,
        >>>                         minimal_value=0,
        >>>                         maximal_value=1,
        >>>                         step=0.1)

        Gives:

        .. figure:: _static/Example_Float_Box.PNG

        """
        super().__init__(label, 0, category)
        self.category = category
        self.entry_name: str = entry_mame
        self.list_of_options: list[Option] = []
        self.add_button: QtW.QPushButton = QtW.QPushButton(self.default_parent)
        self.delete_button: QtW.QPushButton = QtW.QPushButton(self.default_parent)
        self.add_button.clicked.connect(self.add_entry)
        self.delete_button.clicked.connect(self.del_entry)
        self.entries: list[QtW.QFrame] = []

    def add_entry(self) -> None:
        frame: QtW.QFrame = QtW.QFrame(self.category.frame)
        frame.setFrameShape(QtW.QFrame.StyledPanel)
        frame.setFrameShadow(QtW.QFrame.Raised)
        frame.setStyleSheet("QFrame {\n" f"	border: 0px solid {globs.WHITE};\n" "	border-radius: 0px;\n" "  }\n")
        self.entries.append(frame)
        layout = QtW.QHBoxLayout(frame)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QtW.QLabel(self.frame)
        label.setText(self.entry_name)
        layout.addWidget(self.label)
        spacer = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
        layout.addItem(spacer)
        for option in self.list_of_options:
            option = deepcopy(option)
            option.label_text = ""
            option.create_widget(frame, layout)
        self.category.layout_frame.addWidget(self.frame)

    def del_entry(self) -> None:
        entry = self.entries[-1]
        for child in entry.children():
            child.setParent(None)
        entry.setParent(None)

    def get_value(self) -> list[tuple[str, float, int, bool]]:
        """
        This function gets the value of the FloatBox.

        Returns
        -------
        list of values
            Values of the FlexibleAmount
        """
        return self.widget.value()

    def set_value(self, value: list[tuple[str, float, int, bool]]) -> None:
        """
        This function sets the value of the FloatBox.

        Parameters
        ----------
        value : float
            Value to which the FloatBox should be set.

        Returns
        -------
        None
        """
        self.widget.setValue(value)

    def _init_links(self) -> None:
        """
        Function on how the links for the FloatBox should be set.

        Returns
        -------
        None
        """
        current_value: float = self.get_value()
        self.set_value(current_value * 1.1)
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
        return self.minimal_value <= self.get_value() <= self.maximal_value

    def add_link_2_show(
        self,
        option: Option | Category | FunctionButton | Hint,
        below: float = None,
        above: float = None,
    ) -> None:
        """
        This function couples the visibility of an option to the value of the FloatBox object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the FloatBox.
        below : float
            Lower threshold of the FloatBox value below which the linked option will be hidden
        above : float
            Higher threshold of the FloatBox value above which the linked option will be hidden

        Returns
        -------
        None

        Examples
        --------
        This function can be used to couple the FloatBox value to other options, hints, function buttons or categories.
        In the example below, 'option linked' will be shown if the float value is below 0.1 or above 0.9.

        >>> option_float.add_link_2_show(option=option_linked, below=0.1, above=0.9)
        """
        self.linked_options.append((option, (below, above)))
        self.widget.valueChanged.connect(ft_partial(self.show_option, option, below, above))

    def show_option(
        self,
        option: Option | Category | FunctionButton | Hint,
        below: float | None,
        above: float | None,
        args=None,
    ):
        """
        This function shows the option if the value of the FloatBox is between the below and above value.
        If no below or above values are given, no boundary is taken into account for respectively the lower and
        upper boundary.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option to be shown or hidden
        below : float (optional)
            Lower threshold of the FloatBox value below which the linked option will be hidden
        above : float (optional)
            Higher threshold of the FloatBox value above which the linked option will be hidden

        Returns
        -------
        None
        """
        if below is not None and self.get_value() < below:
            return option.show()
        if above is not None and self.get_value() > above:
            return option.show()
        option.hide()

    def check_linked_value(self, value: tuple[float | None, float | None]) -> bool:
        """
        This function checks if the linked "option" should be shown.

        Parameters
        ----------
        value : tuple of 2 optional floats
            first one is the below value and the second the above value

        Returns
        -------
        bool
            True if the linked "option" should be shown
        """
        below, above = value
        if below is not None and self.get_value() < below:
            return True
        if above is not None and self.get_value() > above:
            return True
        return False

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
        self.widget.valueChanged.connect(function_to_be_called)  # pylint: disable=E1101

    def create_widget(
        self,
        frame: QtW.QFrame,
        layout_parent: QtW.QLayout,
        *,
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
            f'QDoubleSpinBox{"{"}selection-color: {globs.WHITE};selection-background-color: {globs.LIGHT};'
            f'border: 1px solid {globs.WHITE};font: {globs.FONT_SIZE}pt "{globs.FONT}";{"}"}'
        )
        self.widget.setAlignment(QtC.Qt.AlignRight | QtC.Qt.AlignTrailing | QtC.Qt.AlignVCenter)
        self.widget.setProperty("showGroupSeparator", True)
        self.widget.setMinimum(self.minimal_value)
        self.widget.setMaximum(self.maximal_value)
        self.widget.setDecimals(self.decimal_number)
        self.widget.setValue(self.default_value)
        self.widget.setSingleStep(self.step)
        if self.limit_size:
            self.widget.setMaximumWidth(100)
            self.widget.setMinimumWidth(100)
        self.widget.setMinimumHeight(28)
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.widget, column, row)
            return
        layout.addWidget(self.widget)
