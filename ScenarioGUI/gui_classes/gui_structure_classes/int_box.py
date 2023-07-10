"""
int box class script
"""
from __future__ import annotations

from functools import partial as ft_partial
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs
from .functions import check_and_set_max_min_values

from ...utils import set_default_font
from .option import Option

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    import PySide6.QtGui as QtG

    from .category import Category
    from .function_button import FunctionButton
    from .hint import Hint


class SpinBox(QtW.QSpinBox):  # pragma: no cover
    def wheelEvent(self, event: QtG.QWheelEvent):
        if self.hasFocus():
            super().wheelEvent(event)
            return
        self.parent().wheelEvent(event)


class IntBox(Option):
    """
    This class contains all the functionalities of the IntBox (integer box) option in the GUI.
    The IntBox can be used to input integer numbers.
    """

    def __init__(
        self,
        label: str | list[str],
        default_value: int,
        category: Category,
        *,
        minimal_value: int = 0,
        maximal_value: int = 100,
        step: int = 1,
    ):
        """

        Parameters
        ----------
        label : str | List[str]
            The label of the IntBox
        default_value : int
            The default value of the IntBox
        category : Category
            Category in which the IntBox should be placed
        minimal_value : int
            Minimal value of the IntBox
        maximal_value : int
            Maximal value of the IntBox
        step : int
            The step by which the value of the IntBox should change when the
            increase or decrease buttons are pressed.

        Examples
        --------
        >>> option_int = IntBox(label="Int label text",  # or self.translations.hint_example if hint_example is in Translation class
        >>>                     default_value=2,
        >>>                     category=category_example,
        >>>                     minimal_value=0,
        >>>                     maximal_value=12,
        >>>                     step=2)

        Gives:

        .. figure:: _static/Example_Int_Box.PNG

        """
        super().__init__(label, default_value, category)
        self.minimal_value: int = minimal_value
        self.maximal_value: int = maximal_value
        self.step: int = step
        self.widget: SpinBox = SpinBox(self.default_parent)

    def get_value(self) -> int:
        """
        This function gets the value of the IntBox.

        Returns
        -------
        int
            Value of the IntBox
        """
        return self.widget.value()

    def set_value(self, value: int) -> None:
        """
        This function sets the value of the IntBox.

        Parameters
        ----------
        value : int
            Value to which the IntBox should be set.

        Returns
        -------
        None
        """
        check_and_set_max_min_values(self.widget, value, self.maximal_value, self.minimal_value)
        self.widget.setValue(value)

    def _init_links(self) -> None:
        """
        Function on how the links for the IntBox should be set.

        Returns
        -------
        None
        """
        current_value: int = self.get_value()
        self.set_value(self.maximal_value if current_value == self.minimal_value else self.minimal_value)
        self.set_value(current_value)

    def _check_value(self) -> bool:
        """
        This function checks if the value of the IntBox is between the minimal_value
        and maximal_value.

        Returns
        -------
        bool
            True if the value is between the minimal and maximal value
        """
        return self.minimal_value <= self.get_value() <= self.maximal_value

    def check_linked_value(self, value: tuple[int | None, int | None]) -> bool:
        """
        This function checks if the linked "option" should be shown.

        Parameters
        ----------
        value : tuple of 2 optional ints
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

    def add_link_2_show(
        self,
        option: Option | Category | FunctionButton | Hint,
        *,
        below: int = None,
        above: int = None,
    ):
        """
        This function couples the visibility of an option to the value of the IntBox object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the IntBox.
        below : int
            Lower threshold of the FloatBox value below which the linked option will be hidden
        above : int
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

    def show_option(
        self,
        option: Option | Category | FunctionButton | Hint,
        below: int | None,
        above: int | None,
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
        below : int (optional)
            Lower threshold of the IntBox value below which the linked option will be hidden
        above : int (optional)
            Higher threshold of the IntBox value above which the linked option will be hidden

        Returns
        -------
        None
        """
        if below is not None and self.get_value() < below:
            return option.show()
        if above is not None and self.get_value() > above:
            return option.show()
        option.hide()

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
            f'QSpinBox{"{"}selection-color: {globs.WHITE};selection-background-color: {globs.LIGHT};'
            f'border: 1px solid {globs.WHITE};{"}"}'
        )
        self.widget.setAlignment(QtC.Qt.AlignRight | QtC.Qt.AlignTrailing | QtC.Qt.AlignVCenter)
        self.widget.setMinimum(self.minimal_value)
        self.widget.setMaximum(self.maximal_value)
        self.widget.setValue(self.default_value)
        self.widget.setSingleStep(self.step)
        self.widget.setMaximumWidth(100)
        self.widget.setMinimumWidth(100)
        self.widget.setMinimumHeight(28)
        self.widget.setFocusPolicy(QtC.Qt.FocusPolicy.StrongFocus)
        set_default_font(self.widget)
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.widget, column, row)
            return
        layout.addWidget(self.widget)
