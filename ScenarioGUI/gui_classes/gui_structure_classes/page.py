"""
page class script
"""
from __future__ import annotations

from functools import partial as ft_partial
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtGui as QtG  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs
from ScenarioGUI.gui_classes.gui_structure_classes.functions import check_aim_options, update_opponent_not_change, update_opponent_toggle

from ...utils import change_font_size, set_default_font
from .aim import Aim

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable

    from .category import Category


class Page:
    """
    This class contains all the functionalities of the Page option in the GUI.
    The Page is the most high-level object of the GUI for it contains Categories and Aims.
    """

    next_label: str = "next"
    previous_label: str = "previous"
    default_parent: QtW.QWidget | None = None
    TOGGLE: bool = True

    def __init__(self, name: str | list[str], button_name: str, icon: str):
        """

        Parameters
        ----------
        name : str | List[str]
            Name of the page (shown on top of the Page)
        button_name : str
            Text to be shown on the button for the Page
        icon : str
            Path to the icon that is used for the Page

        Examples
        --------

        >>> page_example = Page(name="Example page",  #  or self.translations.page_example if page_example is in Translations class
        >>>                     button_name='Name of\\nthe button',
        >>>                     icon="example_icon.svg")

        Gives:

        .. figure:: _static/Example_Page.PNG
        """
        self.name: list[str] = [name] if isinstance(name, str) else name
        self.button_name: str = button_name
        self.icon: str = icon
        self.push_button_next: QtW.QPushButton | None = None
        self.push_button_previous: QtW.QPushButton | None = None
        self.list_categories: list[Category] = []
        self.button: QtW.QPushButton = QtW.QPushButton(self.default_parent)
        self.label: QtW.QLabel = QtW.QLabel(self.default_parent)
        self.label_gap: QtW.QLabel = QtW.QLabel(self.default_parent)
        self.page: QtW.QWidget = QtW.QWidget(self.default_parent)
        self.previous_page: Page | None = None
        self.next_page: Page | None = None
        self.upper_frame: list[Aim] = []
        self.functions_button_clicked: list[Callable] = []
        self.aims_in_row: int = 2

    def add_function_called_if_button_clicked(self, function_to_be_called: Callable) -> None:
        """
        This function calls the function_to_be_called whenever the Page is changed.

        Parameters
        ----------
        function_to_be_called : callable
            Function which should be called

        Returns
        -------
        None
        """
        self.functions_button_clicked.append(function_to_be_called)

    def set_text(self, name: str) -> None:
        """
        This function sets the text of the Page and the page button.

        Parameters
        ----------
        name : str
            String with the text of the button at position 0 and the page name at position 1.
            These strings are separated by ","

        Returns
        -------
        None
        """
        entry_name: list[str, str] = name.split(",")
        self.label.setText(entry_name[1])
        self.button_name = entry_name[0].replace("@", "\n")
        self.button.setText(self.button_name)
        if self.push_button_previous is not None:
            self.push_button_previous.setText(self.previous_label)
        if self.push_button_next is not None:
            self.push_button_next.setText(self.next_label)

    def set_previous_page(self, previous_page: Page) -> None:
        """
        This function sets the previous page.

        Parameters
        ----------
        previous_page : Page
            The page that should be shown when the previous-button is pressed

        Returns
        -------
        None
        """
        self.previous_page = previous_page

    def set_next_page(self, next_page: Page) -> None:
        """
        This function sets the next page.

        Parameters
        ----------
        next_page : Page
            The page that should be shown when the next-button is pressed

        Returns
        -------
        None
        """
        self.next_page = next_page

    def create_page(
        self,
        central_widget: QtW.QWidget,
        stacked_widget: QtW.QStackedWidget,
        vertical_layout_menu: QtW.QVBoxLayout,
    ) -> None:
        """
        This function creates the Page onto the central_widget.

        Parameters
        ----------
        central_widget : QtW.QWidget
            The base framework of the GUI (with the top bar and scenario options) onto which this page should be placed.
        stacked_widget : QtW.QStackedWidget
            The stacked widget in which this page will be placed (all pages are stacked into this stacked_widget)
        vertical_layout_menu : QtW.QVBoxLayout
            The navigation box where all the different page buttons are placed.

        Returns
        -------
        None
        """
        self.page.setParent(central_widget)
        layout = QtW.QVBoxLayout(self.page)
        layout.setSpacing(0)
        self.label.setParent(central_widget)
        label: QtW.QLabel = self.label
        label.setText(self.name[0].split(",")[0])
        set_default_font(label, bold=True, add_2_size=4)
        layout.addWidget(label)
        spacer_label = QtW.QLabel(self.page)
        spacer_label.setMinimumHeight(6)
        spacer_label.setMaximumHeight(6)
        layout.addWidget(spacer_label)
        scroll_area = QtW.QScrollArea(self.page)
        scroll_area.setFrameShape(QtW.QFrame.NoFrame)
        scroll_area.setLineWidth(0)
        scroll_area.setWidgetResizable(True)
        scroll_area_content = QtW.QWidget(scroll_area)
        scroll_area_content.setGeometry(QtC.QRect(0, 0, 864, 695))
        scroll_area.setWidget(scroll_area_content)
        layout.addWidget(scroll_area)
        scroll_area_layout = QtW.QVBoxLayout(scroll_area_content)
        scroll_area_layout.setSpacing(0)
        scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        stacked_widget.addWidget(self.page)
        if self.upper_frame:
            self.create_upper_frame(scroll_area_content, scroll_area_layout)
        label_gap = QtW.QLabel(scroll_area_content)
        label_gap.setMinimumSize(QtC.QSize(0, 6))
        label_gap.setMaximumSize(QtC.QSize(16777215, 6))

        scroll_area_layout.addWidget(label_gap)

        for category in self.list_categories:
            category.create_widget(scroll_area, scroll_area_layout)

        spacer = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Minimum, QtW.QSizePolicy.Expanding)
        scroll_area_layout.addItem(spacer)

        self.create_navigation_buttons(central_widget, layout)

        self.button.setParent(central_widget)
        self.button.setMinimumSize(QtC.QSize(100, 100))
        icon23 = QtG.QIcon()
        icon23.addFile(f"{globs.FOLDER}/icons/{self.icon}", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)
        self.button.setIcon(icon23)
        self.button.setIconSize(QtC.QSize(24, 24))
        self.button.setText(self.button_name)
        set_default_font(self.button, bold=True)
        self.label_gap.setParent(central_widget)
        self.label_gap.setMinimumSize(QtC.QSize(0, 6))
        self.label_gap.setMaximumSize(QtC.QSize(16777215, 6))

        vertical_layout_menu.addWidget(self.button)
        vertical_layout_menu.addWidget(self.label_gap)
        self.button.clicked.connect(ft_partial(stacked_widget.setCurrentWidget, self.page))  # pylint: disable=E1101
        for function_2_be_called in self.functions_button_clicked:
            self.button.clicked.connect(function_2_be_called)  # pylint: disable=E1101

    def set_font_size(self, size: int) -> None:
        """
        set the text size of hint

        Parameters
        ----------
        size: int
            new font size as points
        Returns
        -------

        """
        change_font_size(self.label, size + 4, False)
        change_font_size(self.button, size, False)
        if self.push_button_previous is not None:
            change_font_size(self.push_button_previous, size, False)
        if self.push_button_next is not None:
            change_font_size(self.push_button_next, size, False)

    def create_upper_frame(self, scroll_area_content: QtW.QWidget, scroll_area_layout: QtW.QVBoxLayout):
        """
        This function creates the upper frame of the GUI, i.e. the first visible screen.

        Parameters
        ----------
        scroll_area_content : QtW.QWidget
            Widget in which the upper frame should be created
        scroll_area_layout : QtW.QVBoxLayout
            Layout into which this widget should be placed

        Returns
        -------
        None
        """
        upper_frame = QtW.QFrame(scroll_area_content)
        upper_frame.setStyleSheet(
            f"QFrame {'{'}border: 1px solid {globs.LIGHT};border-top-left-radius: 15px;border-top-right-radius: 15px;"
            f"border-bottom-left-radius: 15px;border-bottom-right-radius: 15px;{'}'}\n"
            f"QLabel{'{'}border: 0px solid {globs.WHITE};{'}'}"
        )
        upper_frame.setFrameShape(QtW.QFrame.StyledPanel)
        upper_frame.setFrameShadow(QtW.QFrame.Raised)
        upper_frame.setSizePolicy(QtW.QSizePolicy.Minimum, QtW.QSizePolicy.Minimum)
        grid_layout = QtW.QGridLayout(upper_frame)
        grid_layout.setVerticalSpacing(6)
        grid_layout.setHorizontalSpacing(6)
        scroll_area_layout.addWidget(upper_frame)
        rows = list(range(self.aims_in_row)) * len(self.upper_frame)
        for idx, option in enumerate(self.upper_frame):
            option.create_widget(upper_frame, grid_layout, (int(idx / self.aims_in_row), rows[idx]))

        list_aims: list[Aim] = [aim for aim in self.upper_frame if isinstance(aim, Aim)]
        if list_aims:
            for idx, aim in enumerate(list_aims):
                default_value = 1 if idx == 0 else 0
                aim.widget.clicked.connect(
                    ft_partial(
                        self.update_function,
                        aim.widget,
                        list_aims[default_value].widget,
                        [aim.widget for i, aim in enumerate(list_aims) if i not in [idx, default_value]],
                    )
                )  # pylint: disable=E1101
                aim.widget.toggled.connect(ft_partial(check_aim_options, list_aims))  # pylint: disable=E1101
            list_aims[0].widget.click()

    def update_function(
        self,
        button: QtW.QPushButton,
        button_opponent: QtW.QPushButton,
        false_button_list: list[QtW.QPushButton] = None,
    ) -> None:
        """
        This function updates which button should be checked/activated or unchecked/deactivated
        This can be done by either the toggle behaviour or not-change behaviour.

        Parameters
        ----------
        button : QtW.QPushButton
            Button which is activated (iff it was not already), and which is deactivated if it was active and is pressed on
        button_opponent : QtW.QPushButton
            Button which is activated if the current button was active and is pressed on
        false_button_list : List[QtW.QPushButton]
            List with other buttons which aren't active

        Returns
        -------
        None
        """
        if self.TOGGLE:
            update_opponent_toggle(button, button_opponent, false_button_list)
            return
        update_opponent_not_change(button, [*false_button_list, button_opponent])

    def create_navigation_buttons(self, central_widget: QtW.QWidget, scroll_area_layout: QtW.QVBoxLayout) -> None:
        """
        This function creates the navigation button (previous and next) on the bottom of each Page.

        Parameters
        ----------
        central_widget : QtW.QWidget

        scroll_area_layout : QtW.QVBoxLayout
            The layout on which parent the navigation buttons will be placed.

        Returns
        -------
        None
        """
        if self.previous_page is None and self.next_page is None:
            return

        horizontal_layout = QtW.QHBoxLayout()

        if self.previous_page is not None:
            self.push_button_previous = QtW.QPushButton(central_widget)
            self.push_button_previous.setMinimumSize(QtC.QSize(0, 30))
            self.push_button_previous.setMaximumSize(QtC.QSize(16777215, 30))
            icon = QtG.QIcon()
            icon.addFile(
                f"{globs.FOLDER}/icons/ArrowLeft.svg",
                QtC.QSize(),
                QtG.QIcon.Normal,
                QtG.QIcon.Off,
            )
            self.push_button_previous.setIcon(icon)
            self.push_button_previous.setIconSize(QtC.QSize(20, 20))
            self.push_button_previous.setText(f"  {self.previous_label}  ")
            set_default_font(self.push_button_previous, bold=True)

            horizontal_layout.addWidget(self.push_button_previous)
            self.push_button_previous.clicked.connect(self.previous_page.button.click)  # pylint: disable=E1101

        horizontal_spacer = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)

        horizontal_layout.addItem(horizontal_spacer)
        if self.next_page is not None:
            self.push_button_next = QtW.QPushButton(central_widget)
            self.push_button_next.setMinimumSize(QtC.QSize(0, 30))
            self.push_button_next.setMaximumSize(QtC.QSize(16777215, 30))
            self.push_button_next.setLayoutDirection(QtC.Qt.RightToLeft)
            icon = QtG.QIcon()
            icon.addFile(
                f"{globs.FOLDER}/icons/ArrowRight.svg",
                QtC.QSize(),
                QtG.QIcon.Normal,
                QtG.QIcon.Off,
            )
            self.push_button_next.setIcon(icon)
            self.push_button_next.setIconSize(QtC.QSize(20, 20))
            self.push_button_next.setText(f"  {self.next_label}  ")
            set_default_font(self.push_button_next, bold=True)

            horizontal_layout.addWidget(self.push_button_next)
            self.push_button_next.clicked.connect(self.next_page.button.click)  # pylint: disable=E1101

        scroll_area_layout.addLayout(horizontal_layout)

    def translate(self, idx: int) -> None:
        """
        Translates the label.

        Parameters
        ----------
        idx: int
            index of language

        Returns
        -------
        None
        """
        self.set_text(self.name[idx])
