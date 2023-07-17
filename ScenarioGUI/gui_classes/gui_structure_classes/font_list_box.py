"""
list box class script
"""
from __future__ import annotations

from functools import partial as ft_partial
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs

from ...utils import set_default_font
from .functions import check
from .list_box import ListBox
from .option import Option

if TYPE_CHECKING:  # pragma: no cover
    import PySide6.QtGui as QtG

    from .category import Category


class FontComboBox(QtW.QFontComboBox):  # pragma: no cover
    def wheelEvent(self, event: QtG.QWheelEvent):
        if self.hasFocus():
            super().wheelEvent(event)
            return
        self.parent().wheelEvent(event)


class FontListBox(ListBox):
    """
    This class contains all the functionalities of the ListBox option in the GUI.
    The ListBox can be used to select one option out of many (sort of like the ButtonBox)
    """

    LinkMatrix: list[int] | None = None

    def __init__(self, label: str | list[str], default_index: int, entries: list[str], category: Category):
        """

        Parameters
        ----------
        label : List[str]
            The label of the ListBox
        default_index : int
            The default index of the ListBox
        entries : List[str]
            The list of all the different buttons in the ListBox
        category : Category
            Category in which the ButtonBox should be placed

        Examples
        --------
        >>> option_list = ListBox(label="List box label text",  # or self.translations.hint_example if hint_example is in Translation class
        >>>                       default_index=0,
        >>>                       entries=['Arial', 'Verdana'],
        >>>                       category=category_example)

        Gives:

        .. figure:: _static/Example_List_Box.PNG

        """
        Option.__init__(self, label, default_index, category)
        self.entries: list[str] = entries
        self.widget: FontComboBox = FontComboBox(self.default_parent)
        self.widget.clear()
        self.widget.addItems(self.entries)
        self._link_matrix: list[int] | None = None

    def link_matrix(self) -> list[int]:
        return [[self.widget.itemText(index) for index in range(self.widget.count())].index(font) for font in self.entries]

    def create_widget(
        self,
        frame: QtW.QFrame,
        layout_parent: QtW.QLayout,
        row: int | None = None,
        column: int | None = None,
    ) -> None:
        """
        This functions creates the ListBox widget in the frame.

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
            f"QFrame {'{'}border: 1px solid {globs.WHITE};border-bottom-left-radius: 0px;border-bottom-right-radius: 0px;{'}'}"
            f"QComboBox{'{'}border: 1px solid {globs.WHITE};border-bottom-left-radius: 0px;border-bottom-right-radius: 0px;{'}'}"
            f"QComboBox QAbstractItemView::item:hover{'{'}color: {globs.WHITE};background-color: {globs.LIGHT_SELECT};{'}'}"
            f"QComboBox QAbstractItemView::item:selected{'{'}color: {globs.WHITE};background-color: {globs.LIGHT_SELECT};{'}'}"
        )
        self.widget.setCurrentIndex(self.link_matrix().index(self.default_value))
        if self.limit_size:
            # self.widget.setMaximumWidth(100)
            self.widget.setMinimumWidth(100)
        self.widget.currentIndexChanged.connect(ft_partial(check, self.linked_options, self))  # pylint: disable=E1101
        self.widget.setMinimumHeight(28)
        self.widget.setFocusPolicy(QtC.Qt.FocusPolicy.StrongFocus)
        set_default_font(self.widget)
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.widget, column, row)
            return
        layout.addWidget(self.widget)
