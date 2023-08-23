"""
int box class script
"""
from __future__ import annotations

from collections.abc import Iterable
from functools import partial as ft_partial
from typing import TYPE_CHECKING

import numpy as np
import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs

from ...utils import set_default_font
from .int_box import SpinBox
from .option import Option
from .functions import check_conditional_visibility

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from .category import Category
    from .function_button import FunctionButton
    from .hint import Hint


class MultipleIntBox(Option):
    """
    This class contains all the functionalities of the IntBox (integer box) option in the GUI.
    The IntBox can be used to input integer numbers.
    """

    def __init__(  # noqa: PLR0913
        self,
        label: str | list[str],
        default_value: Iterable[int],
        category: Category,
        *,
        minimal_value: Iterable[int] | int = 0,
        maximal_value: Iterable[int] | int = 100,
        step: Iterable[int] | int = 1,
    ):
        """

        Parameters
        ----------
        label : str | List[str]
            The label of the IntBox
        default_value : Iterable[int]
            The default value of the IntBox
        category : Category
            Category in which the IntBox should be placed
        minimal_value : Iterable[int] | int
            Minimal value of the IntBox
        maximal_value : Iterable[int] | int
            Maximal value of the IntBox
        step : Iterable[int] | int
            The step by which the value of the IntBox should change when the
            increase or decrease buttons are pressed.

        Examples
        --------
        >>> option_int = MultipleIntBox(label="Int label text",  # or self.translations.option_int if option_int is in Translation class
        >>>                             default_value=(1,2,3),
        >>>                             category=category_example,
        >>>                             minimal_value=0,
        >>>                             maximal_value=(12,11,10),
        >>>                             step=2)

        Gives:

        .. figure:: _static/Example_Int_Box.PNG

        """
        super().__init__(label, default_value, category)
        self.minimal_value: list[int] = [minimal_value for _ in default_value] if not isinstance(minimal_value, Iterable) else minimal_value
        self.maximal_value: list[int] = [maximal_value for _ in default_value] if not isinstance(maximal_value, Iterable) else maximal_value
        self.step: list[int] = [step for _ in default_value] if not isinstance(step, Iterable) else step
        self.widget: list[SpinBox] = [SpinBox(self.default_parent, valueChanged=self.valueChanged.emit) for _ in default_value]

    def get_value(self) -> tuple[int]:
        """
        This function gets the value of the IntBox.

        Returns
        -------
        tuple[int]
            Value of the IntBox
        """
        return tuple(widget.value() for widget in self.widget)

    def set_value(self, value: list[int] | tuple[int]) -> None:
        """
        This function sets the value of the IntBox.

        Parameters
        ----------
        value : list[int]
            Value to which the IntBox should be set.

        Returns
        -------
        None
        """
        _ = [widget.setValue(val) for widget, val in zip(self.widget, value)]

    def _check_value(self) -> bool:
        """
        This function checks if the value of the IntBox is between the minimal_value
        and maximal_value.

        Returns
        -------
        bool
            True if the value is between the minimal and maximal value
        """
        return np.any(np.less_equal(self.minimal_value, self.get_value())) and np.any(np.less_equal(self.get_value(), self.maximal_value))

    def check_linked_value(self, value: tuple[Iterable[int] | None, Iterable[int] | None], value_if_hidden: bool | None = None) -> bool:
        """
        This function checks if the linked "option" should be shown.

        Parameters
        ----------
        value : Iterable of ints
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
            if below is not None and np.any(np.less(self.get_value(), below)):
                return True
            if above is not None and np.any(np.greater(self.get_value(), above)):
                return True
            return False
        return self.check_value_if_hidden(check(), value_if_hidden)

    def create_function_2_check_linked_value(
        self, value: tuple[Iterable[int] | None, Iterable[int] | None], value_if_hidden: bool | None = None
    ) -> Callable[[], bool]:
        """
        creates from values a function to check linked values

        Parameters
        ----------
        value : Iterable of ints
            first one is the below value and the second the above value
        value_if_hidden: bool | None
            the return value, if the option is hidden

        Returns
        -------
        function
        """
        return ft_partial(self.check_linked_value, value, value_if_hidden)

    def add_link_2_show(
        self,
        option: Option | Category | FunctionButton | Hint,
        *,
        below: Iterable[int] | None = None,
        above: Iterable[int] | None = None,
    ):
        """
        This function couples the visibility of an option to the value of the IntBox object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the IntBox.
        below : Iterable[int]
            Lower threshold of the FloatBox value below which the linked option will be hidden
        above : Iterable[int]
            Higher threshold of the FloatBox value above which the linked option will be hidden

        Returns
        -------
        None

        Examples
        --------
        This function can be used to couple the IntBox value to other options, hints, function buttons or categories.
        So in the example `option_linked` will be shown if the integer value is below 1 or above 10.

        >>> option_int.add_link_2_show(option=option_linked, below=1, above=10)
        """
        self.change_event(ft_partial(self.show_option, option, below, above))
        check_conditional_visibility(option)

    def show_option(
        self,
        option: Option | Category | FunctionButton | Hint,
        below: Iterable[int] | None,
        above: Iterable[int] | None,
        args=None,
    ):
        """
        This function shows the option if the value of the IntBox is between the below and above value.
        If no below or above values are given, no boundary is taken into account for respectively the lower and
        upper boundary.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option to be shown or hidden
        below : Iterable[int] (optional)
            Lower threshold of the IntBox value below which the linked option will be hidden
        above : Iterable[int] (optional)
            Higher threshold of the IntBox value above which the linked option will be hidden

        Returns
        -------
        None
        """
        if below is not None and np.any(np.less(self.get_value(), below)):
            return option.show()
        if above is not None and np.any(np.greater(self.get_value(), above)):
            return option.show()
        option.hide()

    def create_widget(
        self,
        frame: QtW.QFrame,
        layout_parent: QtW.QLayout,
        *,
        row: int | None = None,
        column: int | None = None,
    ) -> None:
        """
        This functions creates the IntBox widget in the frame.

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
        for widget, max_val, min_val, step, def_val in zip(self.widget, self.maximal_value, self.minimal_value, self.step, self.default_value):
            widget.setParent(self.frame)
            widget.setStyleSheet(
                f'QSpinBox{"{"}selection-color: {globs.WHITE};selection-background-color: {globs.LIGHT};' f'border: 1px solid {globs.WHITE};{"}"}'
            )
            widget.setAlignment(QtC.Qt.AlignRight | QtC.Qt.AlignTrailing | QtC.Qt.AlignVCenter)
            widget.setMinimum(min_val)
            widget.setMaximum(max_val)
            widget.setValue(def_val)
            widget.setSingleStep(step)
            widget.setMaximumWidth(100)
            widget.setMinimumWidth(100)
            widget.setMinimumHeight(28)
            widget.setFocusPolicy(QtC.Qt.FocusPolicy.StrongFocus)
            set_default_font(widget)
            if row is not None and isinstance(layout_parent, QtW.QGridLayout):
                layout_parent.addWidget(widget, column, row)
                return
            layout.addWidget(widget)
