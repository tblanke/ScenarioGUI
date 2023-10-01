from __future__ import annotations

from functools import partial as ft_partial
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore
import numpy as np

import ScenarioGUI.global_settings as globs
from .float_box import DoubleSpinBox
from .functions import check_and_set_max_min_values, check_conditional_visibility

from ...utils import set_default_font
from .option import Option

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    import PySide6.QtGui as QtG

    from .category import Category
    from .function_button import FunctionButton
    from .hint import Hint


class ArrowDoubleSpinBox(DoubleSpinBox):  # pragma: no cover
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.up = self
        self.down = self
        self.left = self
        self.right = self
        self.setButtonSymbols(QtW.QDoubleSpinBox.NoButtons)

    def set_boxes(self, up: ArrowDoubleSpinBox, down: ArrowDoubleSpinBox, left: ArrowDoubleSpinBox, right: ArrowDoubleSpinBox):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def keyPressEvent(self, event):
        if event.key() == QtC.Qt.Key_Up:
            self.up.setFocus()
            self.up.selectAll()
        elif event.key() == QtC.Qt.Key_Down:
            self.down.setFocus()
            self.down.selectAll()
        elif event.key() == QtC.Qt.Key_Left:
            self.left.setFocus()
            self.left.selectAll()
        elif event.key() == QtC.Qt.Key_Right:
            self.right.setFocus()
            self.right.selectAll()
        else:
            super().keyPressEvent(event)

class MatrixBox(Option):
    """
    This class contains all the functionalities of the MatrixBox option in the GUI.
    The MatrixBox can be used to input floating point numbers in a matrix format.
    """

    def __init__(
        self,
        label: str | list[str],
        default_value: float | list[list[float]],
        category: Category,
        *,
        column: int = 2,
        row: int = 2,
        decimal_number: int | list[list[int]] = 0,
        minimal_value: float | list[list[float]] = 0.0,
        maximal_value: float | list[list[float]] = 1000_000_000.0,
    ):
        """

        Parameters
        ----------
        label : str | List[str]
            The labels of the MatrixBox (first the columns sepereated by , and then the row names)
        default_value : float| list[list[float]]
            The default values of the FloatBoxes
        category : Category
            Category in which the MatrixBox should be placed
        decimal_number : int| list[list[int]]
            Number of decimal points in the FloatBoxes
        minimal_value : float| list[list[float]]
            Minimal values of the FloatBoxes
        maximal_value : float| list[list[float]]
            Maximal values of the FloatBoxes

        Examples
        --------
        >>> option_mat = (label=["Heating peak [kW],Cooling peak [kW],Heating load [kWh],Cooling load [kWh],January,February,March,April,May,June,July,August,September,October,November,December"],
        >>>                            default_value=[[0,1,2,3], [0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,
        >>>                                                                                                                                                 2,3],[0,1,2,3]],
        >>>                            category=self.category_monthly,
        >>>                          row=12,
        >>>                            column=4,
        >>>                            minimal_value=0,
        >>>                            decimal_number=[[3,3,0,0], [3,3,0,0], [3,3,0,0], [3,3,0,0], [3,3,0,0], [3,3,0,0], [3,3,0,0], [3,3,0,0], [3,3,0,0], [3,3,0,0], [3,3,0,0], [3,3,0,0]])

        Gives:

        .. figure:: _static/Example_MatrixBox.PNG

        """
        super().__init__(label, ([[default_value] * column] * row) if isinstance(default_value, float) else default_value, category)
        self.decimal_number: list[list[int]] = ([[decimal_number] * column] * row) if isinstance(decimal_number, int) else decimal_number
        self.minimal_value: list[list[float]] = ([[minimal_value] * column] * row) if isinstance(minimal_value, (float, int)) else minimal_value
        self.maximal_value: list[list[float]] = ([[maximal_value] * column] * row) if isinstance(maximal_value, (float, int)) else maximal_value
        self.column = column
        self.row = row
        self.widget: list[list[ArrowDoubleSpinBox]] = [
            [ArrowDoubleSpinBox(self.default_parent, valueChanged=self.valueChanged.emit) for _ in range(column)] for _ in range(row)
        ]

    def get_value(self) -> list[list[float]]:
        """
        This function gets the value of the FloatBox.

        Returns
        -------
        float
            Value of the FloatBox
        """
        return [[self.widget[r][c].value() for c in range(self.column)] for r in range(self.row)]

    def set_value(self, value: list[list[float]]) -> None:
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
        for row in range(self.row):
            for column in range(self.column):
                check_and_set_max_min_values(self.widget[row][column], value[row][column], self.maximal_value[row][column], self.minimal_value[row][column])
                self.widget[row][column].setValue(value[row][column])

    def _check_value(self) -> bool:
        """
        This function checks if the value of the FloatBox is between the minimal_value
        and maximal_value.

        Returns
        -------
        bool
            True if the value is between the minimal and maximal value
        """
        return np.all(np.array(self.minimal_value) <= np.array(self.get_value())) & np.all(np.array(self.get_value()) <= np.array(self.maximal_value))

    def add_link_2_show(
        self,
        option: Option | Category | FunctionButton | Hint,
        below: list[list[float]] = None,
        above: list[list[float]] = None,
    ) -> None:
        """
        This function couples the visibility of an option to the value of the FloatBox object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the FloatBox.
        below : list[list[float]] (optional)
            Lower threshold of the FloatBox value below which the linked option will be hidden
        above : list[list[float]] (optional)
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
        below: list[list[float]] | None,
        above: list[list[float]] | None,
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
        below : list[list[float]] (optional)
            Lower threshold of the FloatBox value below which the linked option will be hidden
        above : list[list[float]] (optional)
            Higher threshold of the FloatBox value above which the linked option will be hidden

        Returns
        -------
        None
        """
        if below is not None and np.any(np.array(self.get_value()) < np.array(below)):
            return option.show()
        if above is not None and np.any(np.array(self.get_value()) > np.array(above)):
            return option.show()
        option.hide()

    def check_linked_value(self, value: tuple[list[list[float]] | None, list[list[float]] | None], value_if_hidden: bool | None = None) -> bool:
        """
        This function checks if the linked "option" should be shown.

        Parameters
        ----------
        value : tuple of 2 optional float lists
            first one is the below values and the second the above values
        value_if_hidden: bool | None
            the return value, if the option is hidden

        Returns
        -------
        bool
            True if the linked "option" should be shown
        """

        def check() -> bool:
            below, above = value
            if below is not None and np.any(np.array(self.get_value()) < np.array(below)):
                return True
            if above is not None and np.any(np.array(self.get_value()) > np.array(above)):
                return True
            return False

        return self.check_value_if_hidden(check(), value_if_hidden)

    def create_function_2_check_linked_value(
        self,
        value: tuple[list[list[float]] | None, list[list[float]] | None],
        value_if_hidden: bool | None = None,
    ) -> Callable[[], bool]:
        """
        creates from values a function to check linked values

        Parameters
        ----------
        value: tuple[list[list[float]] | None, list[list[float]] | None]
            first one is the below values and the second the above values
        value_if_hidden: bool | None
            the return value, if the option is hidden
        Returns
        -------
        function
        """
        return ft_partial(self.check_linked_value, value, value_if_hidden)

    def set_text(self, name: str) -> None:
        """
        This function sets the label text.

        Parameters
        ----------
        name : str
            Label name of the object

        Returns
        -------
        None
        """
        entry_name: list[str] = name.split(",")

        for idx, label in enumerate(
            [item.widget() for item in [self.frame.layout().itemAtPosition(0, i) for i in range(2, self.column + 2)] if item is not None]
        ):
            label.setText(f"{entry_name[idx]}")
        for idx, label in enumerate([item.widget() for item in [self.frame.layout().itemAtPosition(i, 0) for i in range(1, self.row + 1)] if item is not None]):
            label.setText(f"{entry_name[idx + self.column]}")

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
        self.frame.setStyleSheet("QFrame {\n" f"	border: 0px solid {globs.WHITE};\n" "	border-radius: 0px;\n" "  }\n")
        layout_parent.addWidget(self.frame)
        layout = QtW.QGridLayout(self.frame)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        columns = list(range(self.column)) * 3
        rows = list(range(self.row)) * 3
        for column in range(self.column):
            label = QtW.QLabel(self.frame)
            label.setText("test")
            set_default_font(label)
            layout.addWidget(label, 0, column + 2)

        for row in range(self.row):
            label = QtW.QLabel(self.frame)
            label.setText("test")
            set_default_font(label)
            layout.addWidget(label, row + 1, 0)
            if self.limit_size:
                spacer = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
                layout.addItem(spacer, row + 1, 1)
            for column in range(self.column):
                widget = self.widget[row][column]
                widget.set_boxes(
                    self.widget[rows[self.row + row - 1]][column],
                    self.widget[rows[self.row + row + 1]][column],
                    self.widget[row][columns[self.column + column - 1]],
                    self.widget[row][columns[self.column + column + 1]],
                )
                widget.setParent(self.frame)
                widget.setStyleSheet(
                    f'QDoubleSpinBox{"{"}selection-color: {globs.WHITE};selection-background-color: {globs.LIGHT};' f'border: 1px solid {globs.WHITE};{"}"}'
                )
                widget.setAlignment(QtC.Qt.AlignRight | QtC.Qt.AlignTrailing | QtC.Qt.AlignVCenter)
                widget.setGroupSeparatorShown(True)
                widget.setMinimum(self.minimal_value[row][column])
                widget.setMaximum(self.maximal_value[row][column])
                widget.setDecimals(self.decimal_number[row][column])
                widget.setValue(self.default_value[row][column])
                widget.setSingleStep(0)
                widget.setFocusPolicy(QtC.Qt.FocusPolicy.StrongFocus)
                if self.limit_size:
                    widget.setMaximumWidth(100)
                    widget.setMinimumWidth(100)
                widget.setMinimumHeight(28)
                set_default_font(widget)
                layout.addWidget(widget, row + 1, column + 2)

        self.set_text(self.label_text[0])
