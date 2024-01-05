"""
category class script
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs

from ...utils import set_default_font
from . import Category
from .hint import Hint

if TYPE_CHECKING:  # pragma: no cover
    from .function_button import FunctionButton
    from .option import Option


class Subcategory(Category):
    """
    This class contains all the information for categories - the place where
    options are put.
    """

    default_parent: QtW.QWidget | None = None

    def __init__(self, label: str | list[str], category: Category):
        """

        Parameters
        ----------
        label : str | List[str]
            Label of the category
        category : Category
            Category on which the category should be placed

        Examples
        --------
        >>> category_example = Subcategory(label="Example category",  # or self.translations.category_example if category_example is in Translation class
        >>>                             category=category_example)

        Gives:

        .. figure:: _static/Example_Category.PNG
        """
        self.label_text: list[str] = [label] if isinstance(label, str) else label
        self.frame: QtW.QFrame = QtW.QFrame(self.default_parent)
        self.label: QtW.QLabel = QtW.QLabel(self.frame)
        self.list_of_options: list[Option | Hint | FunctionButton] = []
        self.graphic_left: QtW.QGraphicsView | bool | None = None
        self.graphic_right: QtW.QGraphicsView | bool | None = None
        self.grid_layout: int = 0
        self.layout_frame: QtW.QVBoxLayout | None = None
        category.list_of_options.append(self)
        self.options_hidden = []
        self.conditional_visibility: bool = False

    def create_widget(self, page: QtW.QWidget, layout: QtW.QLayout):
        """
        This function creates the frame for this Category on a given page.
        If the current label text is "", then the frame attribute is set to the given frame.
        It populates this category widget with all the options within this category.

        Parameters
        ----------
        page : QtW.QWidget
            Widget (i.e. page) in which this option should be created
        layout : QtW.QLayout
            The layout parent of the current frame

        Returns
        -------
        None
        """
        frame = QtW.QFrame(page)
        layout_frame_vertical = QtW.QVBoxLayout(frame)
        layout_frame_vertical.setSpacing(0)
        layout_frame_vertical.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)
        frame.setFrameShape(QtW.QFrame.StyledPanel)
        frame.setFrameShadow(QtW.QFrame.Raised)
        frame.setStyleSheet("QFrame {\n" f"	border: 0px solid {globs.WHITE};\n" "	border-radius: 0px;\n" "  }\n")
        super().create_widget(frame, layout_frame_vertical)
