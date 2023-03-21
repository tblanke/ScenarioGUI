"""
float box option class
"""
from __future__ import annotations

from functools import partial
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

    COUNTER: int = 0

    def __init__(
            self,
            label: str,
            default_length: int,
            entry_mame: str,
            category: Category,
            *, 
            min_length: int | None = None,
            max_length: int | None = None,
    ):
        """

        Parameters
        ----------
        label : str
            The label of the Option
        default_length : int
            how many entries should exists per default?
        entry_mame: str
            name of the entries
        category : Category
            Category in which the FloatBox should be placed
        min_length: int | None
            minimal option length
        max_length: int | None
            maximal option length

        Examples
        --------
        >>> option_float = FlexibleAmount(label='flexible option',
        >>>                         default_length=2,
        >>>                         category=category_example,
        >>>                         entry_mame="layer")

        Gives:

        .. figure:: _static/Example_Flexible_Amount.PNG

        """
        super().__init__(label, default_length, category)
        self.category = category
        self.entry_name: str = entry_mame
        self.list_of_options: list[Option] = []
        self.option_entries: list[list[Option]] = []
        self.option_classes: list[tuple[type[Option], dict, str]] = []
        self.func_on_change: Callable[[]] | None = None
        self.len_limits: tuple[int | None, int | None] = (min_length, max_length)
        
    def add_option(self, option: type[Option], name: str, **kwargs):
        self.option_classes.append((option, kwargs, name))

    def _add_entry(self) -> None:
        length = len(self.option_entries)
        label = QtW.QLabel(self.frame)
        label.setText(f"{self.entry_name} {length + 1}")
        self.frame.layout().addWidget(label, length + 1, 0)
        options = []
        i = 2
        for option, kwargs, _ in self.option_classes:
            option_i = option(**kwargs, category=self, label="")
            option_i.change_event(self.func_on_change)
            option_i.create_widget(self.frame, self.frame.layout(), column=length + 1, row=i)
            options.append(option_i)
            i += 1
        self.option_entries.append(options)
        add_button: QtW.QPushButton = QtW.QPushButton(text=" + ", parent=self.frame, clicked=partial(self._add_entry_at_row, row=length))
        delete_button: QtW.QPushButton = QtW.QPushButton(text=" - ", parent=self.frame, clicked=partial(self._del_entry, row=length))
        self.frame.layout().addWidget(add_button, length + 1, i)
        self.frame.layout().addWidget(delete_button, length + 1, i + 1)

    def _add_entry_at_row(self, row: int):
        values = self.get_value()
        values.insert(row + 1, values[row]) if row + 1 < len(values) else values.append(values[row])
        self.set_value(values)
        for option, (min_length, max_length) in self.linked_options:
            self.show_option(option, min_length, max_length)
        self.func_on_change()

    def _del_entry(self, *, row: int | None = None) -> None:
        """
        delete an entry.

        Parameters
        ----------
        row : int | None
            row in which should be deleted (None = last one)

        Returns
        -------
            None
        """
        length = len(self.option_entries)
        row = (length - 1) if row is None else row
        if row == length - 1 == 0:
            return
        values = self.get_value()
        del values[row]
        self.set_value(values)
        for option, (min_length, max_length) in self.linked_options:
            self.show_option(option, min_length, max_length)
        self.func_on_change()

    def get_value(self) -> list[list[str | float | int | bool]]:
        """
        This function gets the value of the FloatBox.

        Returns
        -------
        list of values
            Values of the FlexibleAmount
        """
        return [[option.get_value() for option in option_tuple] for option_tuple in self.option_entries]
    
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
        entry_name: list[str, str] = name.split(",")
        self.label_text = entry_name[0]
        self.label.setText(self.label_text)
        self.entry_name = entry_name[1]
        length = len(self.option_entries)
        for idx, label in enumerate([item.widget() for item in [self.frame.layout().itemAtPosition(i, 0) for i in range(1, length + 1)] 
                                     if item is not None]):
            label.setText(f"{self.entry_name} {idx + 1}")
        for idx, (name, (_, kwargs, _)) in enumerate(zip(entry_name[2:], self.option_classes, strict=False)):
            self.frame.layout().itemAtPosition(0, idx + 2).widget().setText(name)
            self.option_classes[idx] = (self.option_classes[idx][0], self.option_classes[idx][1], name)

    def set_value(self, value: list[list[str, float, int, bool]]) -> None:
        """
        This function sets the value of the Flexible Amount option.

        Parameters
        ----------
        value : list of list of float, int, str, bool
            Value to which the option should be set.

        Returns
        -------
        None
        """
        len_options = len(self.option_entries)
        if len(value) < len_options:
            for length in reversed(range(len(value), len_options)):
                for item in [self.frame.layout().itemAtPosition(length + 1, i) for i in range(len(self.option_classes) + 4)
                             if self.frame.layout().itemAtPosition(length + 1, i) is not None]:
                    item.widget().setParent(None)
                del self.option_entries[length]
        else:
            for _ in range(len_options, len(value)):
                self._add_entry()
                
        self.func_on_change()
        self._init_links()

        for options, values in zip(self.option_entries, value, strict=True):
            for option, val in zip(options, values, strict=True):
                option.set_value(val)

    def _init_links(self) -> None:
        """
        Function on how the links for the FloatBox should be set.

        Returns
        -------
        None
        """
        for option, (min_length, max_length) in self.linked_options:
            self.show_option(option, min_length, max_length)

    def _check_value(self) -> bool:
        """
        This function checks if the value of the Option is between the minimal_length
        and maximal_length.

        Returns
        -------
        bool
            True if the value is between the minimal and maximal length
        """
        return not self.check_linked_value(self.len_limits)

    def add_link_2_show(
            self,
            option: Option | Category | FunctionButton | Hint,
            min_length: int = None,
            max_length: int = None,
    ) -> None:
        """
        This function couples the visibility of an option to the value of the FloatBox object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the FloatBox.
        min_length : int
            length of the Options below which the linked option will be hidden
        max_length : int
            length of the Options above which the linked option will be hidden

        Returns
        -------
        None

        Examples
        --------
        This function can be used to couple the FloatBox value to other options, hints, function buttons or categories.
        In the example below, 'option linked' will be shown if the float value is below 0.1 or above 0.9.

        >>> option_flex.add_link_2_show(option=option_linked, min_length=2, max_length=10)
        """
        self.linked_options.append((option, (min_length, max_length)))

    def show_option(
            self,
            option: Option | Category | FunctionButton | Hint,
            min_length: int | None,
            max_length: int | None,
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
        min_length : int (optional)
            value length of the Option below which the linked option will be hidden
        max_length : int (optional)
            value length of the Option above which the linked option will be hidden

        Returns
        -------
        None
        """
        if min_length is not None and len(self.get_value()) < min_length:
            return option.show()
        if max_length is not None and len(self.get_value()) > max_length:
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
        min_length, max_length = value
        if min_length is not None and len(self.get_value()) < min_length:
            return True
        if max_length is not None and len(self.get_value()) > max_length:
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
        self.func_on_change = function_to_be_called
        for option in self.list_of_options:
            option.change_event(function_to_be_called)

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
        # spacer_label = QtW.QLabel(frame_i)
        # spacer_label.setMinimumHeight(6)
        # spacer_label.setMaximumHeight(6)
        # layout_parent_i.addWidget(spacer_label)
        QtW.QGridLayout(self.frame)

        spacer = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
        self.frame.layout().addItem(spacer)
        i = 2
        for _, _, name in self.option_classes:
            label = QtW.QLabel(frame)
            label.setText(name)
            self.frame.layout().addWidget(label, 0, i)
            i += 1

        _ = [self._add_entry() for _ in range(self.default_value)]
        layout_parent_i.addWidget(self.frame)
