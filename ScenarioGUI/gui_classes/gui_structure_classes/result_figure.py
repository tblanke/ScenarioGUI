"""
result figure class script
"""
from __future__ import annotations

import copy
import logging
import os
from typing import TYPE_CHECKING

import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtGui as QtG  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends import qt_compat
from matplotlib.colors import to_rgb

import ScenarioGUI.global_settings as globs

from ...utils import change_font_size
from . import FunctionButton, IntBox
from .button_box import ButtonBox
from .category import Category
from .font_list_box import FontListBox
from .multiple_int_box import MultipleIntBox

if TYPE_CHECKING:  # pragma: no cover
    from .page import Page


def get_name(font: fm.FontProperties) -> str:
    """
    get the name of the font and catch the MacOS runtime error

    Parameters
    ----------
    font: fm.FontProperties
        font to get name for
    Returns
    -------
        str
    """
    try:
        return font.get_name()
    except RuntimeError:  # pragma: no cover
        return "ZZ"


font_list: list[fm.FontProperties] = [fm.FontProperties(fname=font_path, size=12) for font_path in fm.findSystemFonts()]
font_list = sorted(font_list, key=lambda x: get_name(x))
font_name_set = set()
font_list = [font for font in font_list if get_name(font) not in font_name_set and not font_name_set.add(get_name(font))]


# overwrite navigationToolbar
class NavigationToolbarScenarioGUI(NavigationToolbar):

    def __init__(self, overwrite: bool, canvas, parent, coordinate):
        self.overwrite = overwrite
        super().__init__(canvas, parent, coordinate)

    def save_figure(self, *args):
        if not self.overwrite:
            return super().save_figure(args)
        filetypes = self.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = sorted(filetypes.items())
        default_filetype = self.canvas.get_default_filetype()

        startpath = os.path.expanduser(mpl.rcParams['savefig.directory'])
        start = os.path.join(startpath, self.canvas.get_default_filename())
        filters = []
        selectedFilter = None
        for name, exts in sorted_filetypes:
            exts_list = " ".join(['*.%s' % ext for ext in exts])
            filter = '%s (%s)' % (name, exts_list)
            if default_filetype in exts:
                selectedFilter = filter
            filters.append(filter)
        filters = ';;'.join(filters)

        fname, filter = qt_compat._getSaveFileName(
            self.canvas.parent(), "Choose a filename to save to", start,
            filters, selectedFilter)
        if fname:
            # Save dir for next time, unless empty str (i.e., use cwd).
            if startpath != "":
                mpl.rcParams['savefig.directory'] = os.path.dirname(fname)
            try:
                temp = copy.copy(self.canvas.figure)
                globs.set_print_layout(self.canvas.a_x)
                temp.set_facecolor('white')
                temp.savefig(fname)
            except Exception as e:
                qt_compat.QtWidgets.QMessageBox.critical(
                    self, "Error saving file", str(e),
                    qt_compat._enum("QtWidgets.QMessageBox.StandardButton").Ok,
                    qt_compat._enum("QtWidgets.QMessageBox.StandardButton").NoButton)


class ResultFigure(Category):
    """
    This class contains all the functionalities of the ResultFigure option in the GUI.
    The ResultFigure option can be used to show figurative results in the results page.
    It is a category showing a figure and optionally a couple of FigureOptions to alter this figure.
    """

    def __init__(self, label: str | list[str], page: Page, x_axes_text: str | None = None,
                 y_axes_text: str | None = None, customizable_figure: int = 0):

        """

        Parameters
        ----------
        label : str | List[str]
            Label text of the ResultFigure
        page : Page
            Page where the ResultFigure should be placed (the result page)
        x_axes_text : str
            Text of the x-axes-label
        y_axes_text : str
            Text of the y-axes-label
        customizable_figure : int
            0 if the figure should not be customizable,
            1 if the figure should be automatically saved without a background and with black axes
            2 if the figure should be fully customizable in the gui itself by the user

        Examples
        --------
        The code below generates a ResultFigure category named 'Temperature evolution'.

        >>> self.results_fig = ResultFigure(label="Temperature evolution",  # or self.translations.results_fig if results_fig is in Translation class
        >>>                                 page=self.page_result,
        >>>                                 x_axes_text="x_axes-label",
        >>>                                 y_axes_text="y_axes-label")

        Gives (note that the FigureOption for the legend is also included):

        .. figure:: _static/Example_ResultFigure.PNG
        """
        super().__init__(label, page)
        self.frame_canvas: QtW.QFrame = QtW.QFrame(self.frame)
        self.layout_frame_canvas: QtW.QVBoxLayout = QtW.QVBoxLayout(self.frame_canvas)
        globs.set_graph_layout()
        self.fig: plt.Figure = plt.figure()
        self.a_x: plt.Axes | None = self.fig.add_subplot(111)
        self.canvas: FigureCanvas = FigureCanvas(self.fig)
        self.canvas.a_x = self.a_x
        # create navigation toolbar and replace icons with white ones
        self.toolbar: NavigationToolbarScenarioGUI = NavigationToolbarScenarioGUI(overwrite=customizable_figure==1, canvas=self.canvas, parent=None, coordinate=True)
        for name, icon_name in [
            ("save_figure", "Save_Inv"),
            ("home", "Home"),
            ("zoom", "Search"),
            ("back", "Back"),
            ("forward", "Forward"),
            ("pan", "Pen"),
            ("configure_subplots", "Options"),
            ("edit_parameters", "Parameters"),
        ]:
            icon = QtG.QIcon()
            icon.addFile(
                f"{globs.FOLDER}/icons/{icon_name}.svg",
                QtC.QSize(),
                QtG.QIcon.Normal,
                QtG.QIcon.Off,
            )
            self.toolbar._actions[name].setIcon(icon)
        self._kwargs: dict = {}
        self.function_name: str = ""
        self.class_name: str = ""
        self.x_axes_text: str = "" if x_axes_text is None else x_axes_text
        self.y_axes_text: str = "" if y_axes_text is None else y_axes_text
        self.to_show: bool = True
        self.set_text(self.label_text[0])
        self.scroll_area: QtW.QScrollArea | None = None
        self.customizable_figure: int = customizable_figure

        if customizable_figure == 2:
            self.default_figure_colors = ButtonBox(label="Should the default colors be used?", default_index=1, entries=["No", "Yes"], category=self)
            self.option_figure_background = MultipleIntBox(
                label="Figure background color in rgb code?",
                default_value=np.array(globs.DARK.replace("rgb(", "").replace(")", "").split("," ""), dtype=np.float64),
                category=self,
                minimal_value=0,
                maximal_value=255,
                step=1,
            )
            self.option_plot_background = MultipleIntBox(
                label="Plot background color in rgb code?",
                default_value=np.array(globs.WHITE.replace("rgb(", "").replace(")", "").split("," ""), dtype=np.float64),
                category=self,
                minimal_value=0,
                maximal_value=255,
                step=1,
            )
            self.option_axes_text = MultipleIntBox(
                label="Axes text color in rgb code?",
                default_value=np.array(globs.WHITE.replace("rgb(", "").replace(")", "").split("," ""), dtype=np.float64),
                category=self,
                minimal_value=0,
                maximal_value=255,
                step=1,
            )
            self.option_axes = MultipleIntBox(
                label="Axes color in rgb code?",
                default_value=np.array(globs.WHITE.replace("rgb(", "").replace(")", "").split("," ""), dtype=np.float64),
                category=self,
                minimal_value=0,
                maximal_value=255,
                step=1,
            )
            self.option_title = MultipleIntBox(
                label="Title color in rgb code?",
                default_value=np.array(globs.WHITE.replace("rgb(", "").replace(")", "").split("," ""), dtype=np.float64),
                category=self,
                minimal_value=0,
                maximal_value=255,
                step=1,
            )
            self.option_legend_text = MultipleIntBox(
                label="Legend text color in rgb code?",
                default_value=np.array(globs.DARK.replace("rgb(", "").replace(")", "").split("," ""), dtype=np.float64),
                category=self,
                minimal_value=0,
                maximal_value=255,
                step=1,
            )
            self.option_font_size = IntBox(label="Font Size:", default_value=globs.FONT_SIZE, minimal_value=6, maximal_value=40, category=self)
            self.option_font = FontListBox(
                label="Font family: ",
                category=self,
                entries=[get_name(font) for font in font_list],
                default_index=[get_name(font).upper() for font in font_list].index(globs.FONT.upper()),
            )
            self.option_save_layout = FunctionButton(button_text="Save layout", category=self, icon="Save")
            self.default_figure_colors.add_link_2_show(self.option_figure_background, on_index=0)
            self.default_figure_colors.add_link_2_show(self.option_axes, on_index=0)
            self.default_figure_colors.add_link_2_show(self.option_legend_text, on_index=0)
            self.default_figure_colors.add_link_2_show(self.option_axes_text, on_index=0)
            self.default_figure_colors.add_link_2_show(self.option_plot_background, on_index=0)
            self.default_figure_colors.add_link_2_show(self.option_font_size, on_index=0)
            self.default_figure_colors.add_link_2_show(self.option_title, on_index=0)
            self.default_figure_colors.add_link_2_show(self.option_font, on_index=0)
            self.default_figure_colors.add_link_2_show(self.option_save_layout, on_index=0)
            self.option_figure_background.change_event(self.change_figure_background_color)
            self.option_axes_text.change_event(self.change_axis_text_color)
            self.option_plot_background.change_event(self.change_plot_background_color)
            self.option_axes.change_event(self.change_axes_color)
            self.option_legend_text.change_event(self.change_legend_text_color)
            self.option_font_size.change_event(self.change_font)
            self.option_title.change_event(self.change_title_color)
            self.option_font.change_event(self.change_font)
            self.list_of_options = []

    def replace_figure(self, fig: plt.Figure) -> None:
        """
        Replace figure in canvas and reset toolbar to new figure.

        Parameters
        ----------
        fig: plt.Figure
            matplotlib figure

        Returns
        -------
        None
        """
        plt.close(self.fig)
        self.fig = copy.copy(fig)
        self.a_x = fig.get_axes()[0]
        self.a_x.set_xlabel(self.x_axes_text)
        self.a_x.set_ylabel(self.y_axes_text)
        self.toolbar.home()
        self.canvas.hide()
        self.toolbar.hide()
        canvas = FigureCanvas(self.fig)
        # create navigation toolbar and replace icons with white ones
        toolbar: NavigationToolbarScenarioGUI = NavigationToolbarScenarioGUI(overwrite=self.customizable_figure==1, canvas=canvas, parent=self.frame_canvas, coordinate=True)
        for name, icon_name in [
            ("save_figure", "Save_Inv"),
            ("home", "Home"),
            ("zoom", "Search"),
            ("back", "Back"),
            ("forward", "Forward"),
            ("pan", "Pen"),
            ("configure_subplots", "Options"),
            ("edit_parameters", "Parameters"),
        ]:
            icon = QtG.QIcon()
            icon.addFile(
                f"{globs.FOLDER}/icons/{icon_name}.svg",
                QtC.QSize(),
                QtG.QIcon.Normal,
                QtG.QIcon.Off,
            )
            toolbar._actions[name].setIcon(icon)

        self.layout_frame_canvas.replaceWidget(self.canvas, canvas)
        self.layout_frame_canvas.replaceWidget(self.toolbar, toolbar)

        self.canvas = canvas
        self.canvas.a_x = self.a_x
        self.canvas.mpl_connect("scroll_event", self.scrolling)
        self.toolbar = toolbar
        if self.customizable_figure == 2:
            self.change_figure_background_color()
            self.change_plot_background_color()
            self.change_axis_text_color()
            self.change_axes_color()
            self.change_legend_text_color()
            self.change_title_color()

    def create_widget(self, page: QtW.QScrollArea, layout: QtW.QLayout):
        """
        This function creates the frame for this Category on a given page.
        If the current label text is "", then the frame attribute is set to the given frame.
        It populates this category widget with all the options within this category.

        Parameters
        ----------
        page : QtW.QScrollArea
            Widget (i.e. page) in which this option should be created
        layout : QtW.QLayout
            The layout parent of the current frame

        Returns
        -------
        None
        """
        # create widget as from category
        super().create_widget(page, layout)
        # create frame with no border for the frames inside the NavigationToolbar
        self.frame_canvas.setParent(page)
        self.frame_canvas.setStyleSheet(
            f"QFrame{'{'}border: 0px solid {globs.LIGHT};border-bottom-left-radius: 15px;border-bottom-right-radius: 15px;{'}'}\n"
            f"QLabel{'{'}border: 0px solid {globs.WHITE};{'}'}"
        )
        self.frame_canvas.setFrameShape(QtW.QFrame.StyledPanel)
        self.frame_canvas.setFrameShadow(QtW.QFrame.Raised)
        self.layout_frame.addWidget(self.frame_canvas)
        # set minimal height to ensure a minimal height of the plots
        self.frame_canvas.setMinimumHeight(500)
        # add canvas and toolbar to local frame
        self.layout_frame_canvas.addWidget(self.canvas)
        self.layout_frame_canvas.addWidget(self.toolbar)
        if self.customizable_figure == 2:
            for option in [
                self.default_figure_colors,
                self.option_figure_background,
                self.option_plot_background,
                self.option_axes,
                self.option_axes_text,
                self.option_legend_text,
                self.option_title,
                self.option_font_size,
                self.option_font,
                self.option_save_layout,
            ]:
                option.create_widget(self.frame, self.layout_frame)
                if hasattr(option, "init_links"):
                    option.init_links()
        self.scroll_area = page
        self.canvas.mpl_connect("scroll_event", self.scrolling)

    def change_figure_background_color(self):
        self.fig.set_facecolor(to_rgb(np.array(self.option_figure_background.get_value()) / 255))
        self.canvas.draw()

    def change_plot_background_color(self):
        self.a_x.set_facecolor(to_rgb(np.array(self.option_plot_background.get_value()) / 255))
        self.canvas.draw()

    def change_axes_color(self):
        self.a_x.tick_params(axis="x", colors=to_rgb(np.array(self.option_axes.get_value()) / 255))
        self.a_x.tick_params(axis="y", colors=to_rgb(np.array(self.option_axes.get_value()) / 255))
        self.a_x.spines["top"].set_color(to_rgb(np.array(self.option_axes.get_value()) / 255))
        self.a_x.spines["bottom"].set_color(to_rgb(np.array(self.option_axes.get_value()) / 255))
        self.a_x.spines["left"].set_color(to_rgb(np.array(self.option_axes.get_value()) / 255))
        self.a_x.spines["right"].set_color(to_rgb(np.array(self.option_axes.get_value()) / 255))
        self.canvas.draw()

    def change_title_color(self):
        title = self.a_x.get_title()
        self.a_x.set_title(title, color=to_rgb(np.array(self.option_title.get_value()) / 255))
        self.canvas.draw()

    def change_axis_text_color(self):
        self.a_x.xaxis.label.set_color(to_rgb(np.array(self.option_axes_text.get_value()) / 255))
        self.a_x.yaxis.label.set_color(to_rgb(np.array(self.option_axes_text.get_value()) / 255))
        self.canvas.draw()

    def change_legend_text_color(self):
        legend = self.a_x.get_legend()
        if legend is None:
            return
        for text in legend.get_texts():
            text.set_color(to_rgb(np.array(self.option_legend_text.get_value()) / 255))
        self.canvas.draw()

    def change_font(self):
        font: fm.FontProperties = font_list[self.option_font.get_value()[0]]
        font.set_size(self.option_font_size.get_value())

        self.a_x.set_xlabel(self.a_x.get_xlabel(), fontproperties=font)
        self.a_x.set_ylabel(self.a_x.get_ylabel(), fontproperties=font)
        _ = [label.set_fontproperties(font) for label in self.a_x.get_xticklabels()]
        _ = [label.set_fontproperties(font) for label in self.a_x.get_yticklabels()]
        if self.a_x.get_title() is not None:
            self.a_x.set_title(self.a_x.get_title(), fontproperties=font)
        legend = self.a_x.get_legend()
        if legend is not None:
            for text in legend.get_texts():
                text.set_font_properties(font)
        self.canvas.draw()

    def scrolling(self, event) -> None:
        """
        This function handels the scrolling behaviour.

        Parameters
        ----------
        event : Event

        Returns
        -------
        None
        """
        val = self.scroll_area.verticalScrollBar().value()
        if event.button == "down":
            self.scroll_area.verticalScrollBar().setValue(val + self.scroll_area.verticalScrollBar().singleStep())
            return
        self.scroll_area.verticalScrollBar().setValue(val - self.scroll_area.verticalScrollBar().singleStep())

    def set_text(self, name: str) -> None:
        """
        This function sets the text in the Figure category label and function button (separated by comma).

        Parameters
        ----------
        name : str
            Name of the Figure category label and function button.\n
            These strings are separated by ","

        Returns
        -------
        None
        """
        entry_name: list[str, str] = name.split(",")
        self.label.setText(entry_name[0])
        self.y_axes_text: str = entry_name[1]
        self.x_axes_text: str = entry_name[2]
        self.a_x.set_xlabel(self.x_axes_text)
        self.a_x.set_ylabel(self.y_axes_text)

    def fig_to_be_shown(
        self,
        class_name: str,
        function_name: str,
        **kwargs,
    ) -> None:
        """
        This function sets the result that should be shown. It refers to a certain function (function_name) inside the class class_name.
        It is possible to pass through fixed arguments to this function by using **kwargs.
        Arguments that do change, have to be set using a FigureOption.

        Parameters
        ----------
        class_name : str
            The class which contains the variable that should be shown (currently only Borefield)
        function_name : str
            Function that creates the figure. This should be a function existing in the class_name Class.
        **kwargs : dict
            A dictionary with keys being the function arguments which have preset values and the corresponding value.

        Returns
        -------
        None

        Examples
        --------
        The example below shows the temperature profile by calling on the 'print_temperature_profile' function in the Borefield class.

        >>> self.figure_temperature_profile.fig_to_be_shown(class_name="Borefield",
        >>>                                                 function_name="print_temperature_profile")
        """
        self.class_name = class_name
        self.function_name = function_name
        self._kwargs = kwargs

    @property
    def kwargs(self) -> dict:
        """
        This function returns the argument-value pairs for the function that generates the figure
        for this ResultFigure.

        Returns
        -------
        dict
            Dictionary with all the argument names (as keys) and the corresponding values
        """
        kwargs_temp = {}
        for i in self.list_of_options:
            if not i.is_hidden():
                key, value = i.get_value()
                kwargs_temp[key] = value
        return {**self._kwargs, **kwargs_temp}

    def show(self, results: bool = False) -> None:
        """
        This function shows the ResultFigure option.
        It makes sure that the figure is not shown when loading the entire GUI,
        but only when the result page is opened.

        Parameters
        ----------
        results : bool
            True if this function is called w.r.t. result page

        Returns
        -------
        None
        """
        if self.to_show:
            super().show()
        if results:
            return
        self.to_show = True

    def set_font_size(self, size: int) -> None:
        """
        set the new font size to button

        Parameters
        ----------
        size: new font size in points

        Returns
        -------
            None
        """
        change_font_size(self.label, size)
        self.option_font_size.set_font_size(size)
        self.option_font.set_font_size(size)
        self.option_title.set_font_size(size)
        self.option_axes.set_font_size(size)
        self.option_figure_background.set_font_size(size)
        self.option_save_layout.set_font_size(size)
        self.option_plot_background.set_font_size(size)
        self.option_legend_text.set_font_size(size)
        self.default_figure_colors.set_font_size(size)
        self.option_axes_text.set_font_size(size)

    def hide(self, results: bool = False) -> None:
        """
        This function hides the ResultFigure option.
        It also sets the to_show parameter to False, so the Figure is not randomly showed
        when the result page is opened.

        Parameters
        ----------
        results : bool
            True if the hide function is called w.r.t. result page

        Returns
        -------
        None
        """
        super().hide()
        if results:
            return
        self.to_show = False
