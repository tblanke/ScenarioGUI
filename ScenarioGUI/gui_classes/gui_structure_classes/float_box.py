"""
float box option class
"""
from __future__ import annotations

from functools import partial as ft_partial
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtGui as QtG
import PySide6.QtWidgets as QtW  # type: ignore
import numpy as np

import ScenarioGUI.global_settings as globs

from ...utils import set_default_font
from .functions import check_and_set_max_min_values, check_conditional_visibility
from .option import Option

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from .category import Category
    from .function_button import FunctionButton
    from .hint import Hint


class DoubleSpinBox(QtW.QDoubleSpinBox):  # pragma: no cover
    def wheelEvent(self, event: QtG.QWheelEvent):
        if self.hasFocus():
            super().wheelEvent(event)
            return
        self.parent().wheelEvent(event)

    def validate(self, float_str: str, pos: int) -> object:
        """
        validates the float str and makes the numbers behind the decimal point set able

        Parameters
        ----------
        float_str: str
            string of the float inside the double spin box
        pos: int
            position of cursor inside the double spin box

        Returns
        -------
            object
        """
        # get sign and decimal symbols
        decimal_sign = self.locale().decimalPoint()
        sep_sign = self.locale().groupSeparator()
        has_sep = sep_sign in float_str
        len_bef = float_str[:pos].count(sep_sign)
        if pos > len(float_str) or float_str == "":
            return QtW.QDoubleSpinBox.validate(self, float_str, pos)
        is_number = not (float_str[pos-1] in [sep_sign, decimal_sign])
        if decimal_sign not in float_str and self.decimals() > 0:
            float_str += decimal_sign
            float_str += "0" * self.decimals()
        # move the curser to the next number if the current one is not
        # float_str = float_str.replace(sep_sign, "")
        nb_of_chars = len(float_str) - 1 if decimal_sign in float_str else 0
        nb_of_decimals = 0 if decimal_sign not in float_str else nb_of_chars - float_str.index(decimal_sign)
        # overwrite decimals
        if nb_of_decimals > self.decimals() and pos != nb_of_chars + 1:
            float_str = float_str[:-1]
        # move values if the current one is above the maximum
        limit_reached: bool = False
        if self.maximum() > 1 or self.minimum() < -1:
            float_str = float_str.replace(sep_sign, "")
            strings = float_str.split(decimal_sign)
            strings[0] = "0" if strings[0] == "" else strings[0]
            strings[0] = "-0" if strings[0] == "-" else strings[0]
            new_float_str = f"{strings[0]}.{strings[1]}" if len(strings) > 1 else strings[0]
            limit_reached = (float(new_float_str) > self.maximum() and float(new_float_str) > 0) or float(new_float_str) < self.minimum()
            if limit_reached:
                float_str = f"{strings[0][:-1]}{decimal_sign}{strings[0][-1]}{strings[1][:-1]}" if len(strings) > 0 else strings[:-1]
            if has_sep:
                minus = float_str[0] == "-"
                if minus:
                    float_str = float_str[1:]
                dec_idx = float_str.index(decimal_sign) if self.decimals() > 0 and float_str.index(decimal_sign) > 2 else 0
                # Initialize an empty result string
                result_string = ""
                # Iterate through the original string in reverse
                for i, char in enumerate(reversed(float_str[: dec_idx])):
                    # Check if it's time to insert the symbol
                    if i > 0 and i % 3 == 0:
                        result_string = sep_sign + result_string  # Insert the symbol
                    result_string = char + result_string  # Add the character
                float_str = result_string + float_str[dec_idx:]
                if minus:
                    float_str = f"-{float_str}"
        pos = (pos + 1) if limit_reached and is_number and float_str[pos-1] == decimal_sign else pos
        pos = (pos + 1) if len_bef < float_str[:pos].count(sep_sign) else pos
        pos = (pos - 1) if len_bef > float_str[:pos].count(sep_sign) else pos
        return QtW.QDoubleSpinBox.validate(self, float_str, pos)


class FloatBox(Option):
    """
    This class contains all the functionalities of the FloatBox option in the GUI.
    The FloatBox can be used to input floating point numbers.
    """

    def __init__(  # noqa: PLR0913
            self,
            label: str | list[str],
            default_value: float,
            category: Category,
            *,
            decimal_number: int = 0,
            minimal_value: float = 0.0,
            maximal_value: float = 100.0,
            step: float = 1.0,
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

        Examples
        --------
        >>> option_float = FloatBox(label="Float label text",  # or self.translations.option_float if option_float is in Translation class
        >>>                         default_value=0.5,
        >>>                         category=category_example,
        >>>                         decimal_number=2,
        >>>                         minimal_value=0,
        >>>                         maximal_value=1,
        >>>                         step=0.1)

        Gives:

        .. figure:: _static/Example_Float_Box.PNG

        """
        super().__init__(label, default_value, category)
        self.decimal_number: int = decimal_number
        self.minimal_value: float = minimal_value
        self.maximal_value: float = maximal_value
        self.step: float = step
        self.widget: DoubleSpinBox = DoubleSpinBox(self.default_parent, valueChanged=self.valueChanged.emit)

    def get_value(self) -> float:
        """
        This function gets the value of the FloatBox.

        Returns
        -------
        float
            Value of the FloatBox
        """
        return self.widget.value()

    def set_value(self, value: float) -> None:
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
        check_and_set_max_min_values(self.widget, value, self.maximal_value, self.minimal_value)
        self.widget.setValue(value)

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
        self.change_event(ft_partial(self.show_option, option, below, above))
        check_conditional_visibility(option)

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

    def check_linked_value(self, value: tuple[float | None, float | None], value_if_hidden: bool | None = None) -> bool:
        """
        This function checks if the linked "option" should be shown.

        Parameters
        ----------
        value : tuple of 2 optional floats
            first one is the below value and the second the above value
        value_if_hidden: bool | None
            the return value, if the option is hidden

        Returns
        -------
        bool
            True if the linked "option" should be shown
        """

        def check() -> bool:
            below, above = value
            if below is not None and self.get_value() < below:
                return True
            if above is not None and self.get_value() > above:
                return True
            return False

        return self.check_value_if_hidden(check(), value_if_hidden)

    def create_function_2_check_linked_value(self, value: tuple[float | None, float | None], value_if_hidden: bool | None = None) -> Callable[[], bool]:
        """
        creates from values a function to check linked values

        Parameters
        ----------
        value : tuple of 2 optional floats
            first one is the below value and the second the above value
        value_if_hidden: bool | None
            the return value, if the option is hidden

        Returns
        -------
        function
        """
        return ft_partial(self.check_linked_value, value, value_if_hidden)

    def create_widget(
            self,
            frame: QtW.QFrame,
            layout_parent: QtW.QLayout,
            *,
            row: int | None = None,
            column: int | None = None,
    ) -> None:
        """
        This functions creates the FloatBox widget in the frame.

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
        layout = self.create_frame(frame, layout_parent)
        self.widget.setParent(self.frame)
        self.widget.setStyleSheet(
            f'QDoubleSpinBox{"{"}selection-color: {globs.WHITE};selection-background-color: {globs.LIGHT};' f'border: 1px solid {globs.WHITE};{"}"}'
        )
        self.widget.setAlignment(QtC.Qt.AlignRight | QtC.Qt.AlignTrailing | QtC.Qt.AlignVCenter)
        self.widget.setGroupSeparatorShown(True)
        self.widget.setMinimum(self.minimal_value)
        self.widget.setMaximum(self.maximal_value)
        self.widget.setDecimals(self.decimal_number)
        self.widget.setValue(self.default_value)
        self.widget.setSingleStep(self.step)
        self.widget.setFocusPolicy(QtC.Qt.FocusPolicy.StrongFocus)
        if self.limit_size:
            self.widget.setMaximumWidth(100)
            self.widget.setMinimumWidth(100)
        self.widget.setMinimumHeight(28)
        set_default_font(self.widget)
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.widget, column, row)
            return
        layout.addWidget(self.widget)
