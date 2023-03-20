"""
float box option class
"""
from __future__ import annotations

from functools import partial
from functools import partial as ft_partial
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore
import ScenarioGUI.global_settings as globs

from .option import Option

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
        self.entries: list[QtW.QFrame] = []
        self.option_entries: list[list[Option]] = []
        self.option_classes: list[tuple[type[Option], dict, str]] = []
        self.buttons: list[tuple[QtW.QPushButton, QtW.QPushButton]] = []
        
    def add_option(self, option: type[Option], name: str, **kwargs):
        self.option_classes.append((option, kwargs, name))

    def _add_entry(self) -> None:
        length = len(self.option_entries)
        print(f'Here{len(self.option_entries)}')
        label = QtW.QLabel(self.frame)
        label.setText(f"{self.entry_name} {length + 1}")
        self.frame.layout().addWidget(label, length + 1, 0)
        options = []
        i = 2
        for option, kwargs, _ in self.option_classes:
            option_i = option(**kwargs, category=self, label="")
            option_i.label_text = ""
            option_i.create_widget(self.frame, self.frame.layout(), column= length + 1, row=i)
            options.append(option_i)
            i+=1
        self.option_entries.append(options)
        add_button: QtW.QPushButton = QtW.QPushButton(self.default_parent)
        delete_button: QtW.QPushButton = QtW.QPushButton(self.default_parent)
        add_button.setText(" + ")
        delete_button.setText(" - ")
        add_button.clicked.connect(self._add_entry)
        delete_button.clicked.connect(partial(self._del_entry, button=delete_button))
        self.frame.layout().addWidget(add_button, length + 1, i)
        self.frame.layout().addWidget(delete_button, length + 1, i + 1)
        self.buttons.append((add_button, delete_button))

    def _del_entry(self, *, button: QtW.QPushButton | None = None) -> None:
        length = len(self.option_entries)
        idx = [idx for idx, (_, but) in enumerate(self.buttons) if but == button]
        row = length if button is None else length if not idx else idx[0]
        print(f"row: {row}, {len(self.buttons)}")
        if row == length and row == 0:
            return
        values = self.get_value()
        print(f"row: {row}, {len(self.buttons)}, values {len(values)}")
        del values[row]
        self.set_value(values)

    def get_value(self) -> list[list[str | float | int | bool]]:
        """
        This function gets the value of the FloatBox.

        Returns
        -------
        list of values
            Values of the FlexibleAmount
        """
        return [[option.get_value() for option in option_tuple] for option_tuple in self.option_entries]

    def set_value(self, value: list[list[str, float, int, bool]]) -> None:
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
        len_options = len(self.option_entries)
        if len(value) < len_options:
            for length in range(len(value), len_options):
                for item in [self.frame.layout().itemAtPosition(length, i) for i in range(len(self.option_classes) + 4)
                             if self.frame.layout().itemAtPosition(length, i) is not None]:

                    item.widget().setParent(None)
                del self.option_entries[length]
            #for length in reversed(range(len(value), len_options)):
            self.buttons = self.buttons[:len(value)]
        else:
            for _ in range(len_options, len(value) + 1):
                self._add_entry()
        print(len(value), len_options)
        for options, values in zip(self.option_entries, value, strict=True):
            for option, val in zip(options, values, strict=True):
                option.set_value(val)

        #[[option.set_value(value) for option in option_tuple] for option_tuple in self.option_entries]

    def _init_links(self) -> None:
        """
        Function on how the links for the FloatBox should be set.

        Returns
        -------
        None
        """
        return
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
        return
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
        return 
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
        return 
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
        return False
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
        return 
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
        frame_i = QtW.QFrame(frame)
        frame_i.setFrameShape(QtW.QFrame.StyledPanel)
        frame_i.setFrameShadow(QtW.QFrame.Raised)
        frame_i.setStyleSheet("QFrame {\n" f"	border: 0px solid {globs.WHITE};\n" "	border-radius: 0px;\n" "  }\n")
        layout_parent.addWidget(frame_i)
        layout_parent_i = QtW.QVBoxLayout(frame_i)
        layout_parent_i.setSpacing(0)
        layout_parent_i.setContentsMargins(0, 0, 0, 0)
        self.label.setParent(frame_i)
        self.label.setText(self.label_text)
        self.label.setStyleSheet(
            f"QLabel {'{'}border: 1px solid  {globs.LIGHT};border-top-left-radius: 15px;border-top-right-radius: 15px;"
            f"border-bottom-left-radius: 0px;border-top-bottom-radius: 0px;"
            f"background-color:  {globs.LIGHT};padding: 5px 0px;\n"
            f"	color:  {globs.WHITE};font-weight:700;{'}'}"
        )
        self.label.setAlignment(QtC.Qt.AlignCenter | QtC.Qt.AlignVCenter)
        layout_parent_i.addWidget(self.label)
        self.frame.setParent(frame_i)
        self.frame.setStyleSheet(
            f"QFrame{'{'}border: 1px solid {globs.LIGHT};border-bottom-left-radius: 15px;border-bottom-right-radius: 15px;{'}'}\n"
            f"QLabel{'{'}border: 0px solid {globs.WHITE};{'}'}"
        )
        self.frame.setFrameShape(QtW.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtW.QFrame.Raised)
        layout_parent_i.addWidget(self.frame)
        #spacer_label = QtW.QLabel(frame_i)
        #spacer_label.setMinimumHeight(6)
        #spacer_label.setMaximumHeight(6)
        #layout_parent_i.addWidget(spacer_label)
        QtW.QGridLayout(self.frame)
        
        spacer = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
        self.frame.layout().addItem(spacer)
        i = 2
        for _, _, name in self.option_classes:
            label = QtW.QLabel(frame)
            label.setText(name)
            self.frame.layout().addWidget(label, 0, i)
            i+=1
            
        self._add_entry()
        layout_parent_i.addWidget(self.frame)
