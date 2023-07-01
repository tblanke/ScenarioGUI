from __future__ import annotations

from math import log10
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as globs
from ScenarioGUI.utils import change_font_size, set_default_font

from .float_box import FloatBox
from .list_box import ComboBox

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from . import FunctionButton, Hint, Option
    from .category import Category


class FloatBoxWithUnits(FloatBox):
    """Int box with units as Combobox"""

    def __init__(
        self,
        label: str | list[str],
        default_value: float,
        category: Category,
        *,
        decimal_number: int = 0,
        minimal_value: float = 0.0,
        maximal_value: float = 100.0,
        step: float = 1.0,
        units: list[tuple[str, float]] | None = None
    ):
        """

        Parameters
        ----------
        label : str | List[str]
            The label of the FloatBox
        default_value : float
            The default value of the FloatBox
        category : Category
            Category in which the FloatBox should be placed
        decimal_number : int
            Number of decimal points in the FloatBox
        minimal_value : float
            Minimal value of the FloatBox
        maximal_value : float
            Maximal value of the FloatBox
        step : float
            The step by which the value of the FloatBox should change when the
            increase or decrease buttons are pressed.
        units: list[tuple[str, float]]
            The list of units with its names and thier scaling factors

                Examples
        --------
        >>> option_float = FloatBoxWithUnits(label="Float label text",  # or self.translations.option_float if option_float is in Translation class
        >>>                         default_value=0.5,
        >>>                         category=category_example,
        >>>                         decimal_number=2,
        >>>                         minimal_value=0,
        >>>                         maximal_value=1,
        >>>                         step=0.1,
        >>>                         units=[("kW", 1), ("W", 0.001), ("MW", 1_000)])

        Gives:

        .. figure:: _static/Example_Float_Box_With_Units.PNG
        """
        super().__init__(label=label, default_value=default_value, category=category, maximal_value=maximal_value, minimal_value=minimal_value, step=step,
                         decimal_number=decimal_number)
        self.units: list[tuple[str, float]] = [] if units is None else units
        self.unit_widget: ComboBox = ComboBox(self.default_parent)

    def activate_scale_decimals(self) -> None:
        """
        activates that the decimal number is scaled with the units in the drop down menu

        Returns
        -------
            None
        """
        self.unit_widget.currentIndexChanged.connect(self._change_decimals)

    def _change_decimals(self):
        unit = self.units[self.unit_widget.currentIndex()][1]
        self.widget.setDecimals(log10(unit) + self.decimal_number)

    def get_value(self) -> tuple[float, int]:
        """
        This function gets the value of the IntBox.

        Returns
        -------
        tuple[float, int]
            Value of the IntBox multiplied with units value and unit box index
        """
        return self.widget.value() * self.units[self.unit_widget.currentIndex()][1], self.unit_widget.currentIndex()

    def set_value(self, value: tuple[float, int]) -> None:
        """
        This function sets the value of the IntBox.

        Parameters
        ----------
        value : tuple[float, int]
            Value to which the IntBox should be set and unit widget index

        Returns
        -------
        None
        """
        self.unit_widget.setCurrentIndex(value[1])
        self.widget.setValue(value[0] / self.units[value[1]][1])

    def _init_links(self) -> None:
        """
        Function on how the links for the FloatBox should be set.

        Returns
        -------
        None
        """
        current_index: int = self.unit_widget.currentIndex() if self.unit_widget.currentIndex() > 0 else 0
        current_value: float = self.get_value()[0] / self.units[current_index][1]
        self.set_value((current_value * 1.1, current_index + 1))
        self.set_value((current_value, current_index))

    def _check_value(self) -> bool:
        """
        This function checks if the value of the IntBox is between the minimal_value
        and maximal_value.

        Returns
        -------
        bool
            True if the value is between the minimal and maximal value
        """
        value = self.get_value()
        return self.minimal_value <= value[0] / self.units[value[1]][1] <= self.maximal_value

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
        if below is not None and self.get_value()[0] < below:
            return option.show()
        if above is not None and self.get_value()[0] > above:
            return option.show()
        option.hide()

    def set_font_size(self, size: int) -> None:
        """
        scale the font size

        Parameters
        ----------
        size: int
            new font size
        """
        super().set_font_size(size)
        change_font_size(self.unit_widget, size, True)

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
        if below is not None and self.get_value()[0] < below:
            return True
        if above is not None and self.get_value()[0] > above:
            return True
        return False

    def change_event(self, function_to_be_called: Callable) -> None:
        """
        This function calls the function_to_be_called whenever the IntBox is changed.

        Parameters
        ----------
        function_to_be_called : callable
            Function which should be called

        Returns
        -------
        None
        """
        self.widget.valueChanged.connect(function_to_be_called)  # pylint: disable=E1101
        self.unit_widget.currentIndexChanged.connect(function_to_be_called)  # pylint: disable=E1101

    def create_widget(
            self,
            frame: QtW.QFrame,
            layout_parent: QtW.QLayout,
            *,
            row: int = None,
            column: int = None,
    ) -> None:
        """
        This functions creates the IntBox widget in the frame.

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
        super().create_widget(frame, layout_parent, row=row, column=column)
        self.unit_widget.setParent(self.frame)
        self.frame.layout().addWidget(self.unit_widget)
        self.unit_widget.addItems([name for name, _ in self.units])
        self.unit_widget.setStyleSheet(
            f"QFrame {'{'}border: 1px solid {globs.WHITE};border-bottom-left-radius: 0px;border-bottom-right-radius: 0px;{'}'}"
            f"QComboBox{'{'}border: 1px solid {globs.WHITE};border-bottom-left-radius: 0px;border-bottom-right-radius: 0px;{'}'}"
            f"QComboBox QAbstractItemView::item:hover{'{'}color: {globs.WHITE};background-color: {globs.LIGHT_SELECT};{'}'}"
            f"QComboBox QAbstractItemView::item:selected{'{'}color: {globs.WHITE};background-color: {globs.LIGHT_SELECT};{'}'}"
        )
        self.unit_widget.setMinimumHeight(self.widget.minimumHeight())
        self.unit_widget.setFocusPolicy(QtC.Qt.FocusPolicy.StrongFocus)
        set_default_font(self.unit_widget)


