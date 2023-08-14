from __future__ import annotations

import datetime
import logging
from functools import partial as ft_partial
from json import dump, load
from os import makedirs, remove
from os.path import dirname, exists, realpath
from os.path import split as os_split
from os.path import splitext
from pathlib import Path
from sys import path
from typing import TYPE_CHECKING, TypedDict

import PySide6.QtCore as QtC
import PySide6.QtGui as QtG
import PySide6.QtWidgets as QtW
from matplotlib import rcParams

import ScenarioGUI.global_settings as globs
from ScenarioGUI.gui_classes.gui_structure_classes.functions import check_aim_options

from ..utils import change_font_size, set_default_font
from .gui_base_class import BaseUI
from .gui_calculation_thread import CalcProblem
from .gui_data_storage import DataStorage
from .gui_saving_thread import SavingThread
from .gui_structure_classes import FigureOption, Option, ResultExport

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Protocol

    from ScenarioGUI.gui_classes.gui_structure import GuiStructure

    from .translation_class import Translations

    class ResultsClass(Protocol):
        """Testing"""

        def to_dict(self) -> dict:
            """creates a dict from class data"""

        @staticmethod
        def from_dict(dictionary: dict) -> ResultsClass:
            """creates a class from dict data"""


currentdir = dirname(realpath(__file__))
parentdir = dirname(currentdir)
path.append(parentdir)


class JsonDict(TypedDict, total=True):
    filename: tuple[str, str]
    names: list[str]
    version: str
    values: list[dict]
    results: list[dict]


def normal_export(file_path: Path, data: dict):
    """
    normal export function

    Parameters
    ----------
    file_path: Path
        path to file including the file and type
    data: dict
        json dict of data

    Returns
    -------
        None
    """
    # write data to back up file
    with open(file_path, "w") as file:
        dump(data, file, indent=1)


def normal_import(location: Path) -> JsonDict:
    """
    normal import function from json

    Parameters
    ----------
    location: Path
        path to file including the file and type
    Returns
    -------
        JsonDict
    """
    # open file and get data
    with open(location) as file:
        saving = load(file)

    return saving


# main GUI class
class MainWindow(QtW.QMainWindow, BaseUI):
    """
    This class contains the general functionalities of the GUI (e.g. the handling of creating new scenarios,
    saving documents etc.)
    """

    filename_default: tuple = ("", "")
    role: int = 99
    TEST_MODE: bool = False
    button_width_large: int = 150
    button_width_small: int = 75
    button_height: int = 75
    icon_size_small: int = 24
    icon_size_large: int = 48

    def __init__(  # noqa: PLR0913
        self,
        dialog: QtW.QWidget,
        app: QtW.QApplication,
        gui_structure: type[GuiStructure],
        translations: type[Translations],
        *,
        result_creating_class: type[ResultsClass],
        data_2_results_function: Callable[
            [DataStorage],
            tuple[object, ft_partial[[], None]] | tuple[object, Callable[[], None]],
        ],
    ) -> MainWindow:
        """

        Parameters
        ----------
        dialog : QtW.QWidget
            Q widget as main window where everything is happening
        app : QtW.QApplication
            The widget for the application itself
        result_creating_class: Object with from_dict and to_dict function
            results creating class
        data_2_results_function : Callable
            function to create the results class and a function to be called in the thread

        Returns
        -------
        MainWindow
        """
        # parameter to show the end of the init function
        self._backup_filename: str = f"backup.{globs.FILE_EXTENSION}BackUp"
        # init windows of parent class
        super().__init__()
        # get the current screen to determine its size
        current_screen = QtG.QGuiApplication.primaryScreen() if QtG.QGuiApplication.primaryScreen() is not None else QtG.QGuiApplication.screens()[0]
        super().setup_ui(dialog, current_screen.size(), globs.GUI_NAME)
        # pyside6-rcc icons.qrc -o icons_rc.py
        self.translations: Translations = translations()  # init translation class

        self.result_creating_class = result_creating_class
        self.data_2_results_function = data_2_results_function

        self.gui_structure = gui_structure(self.central_widget, self.translations)

        [page.create_page(self.central_widget, self.stacked_widget, self.vertical_layout_menu) for page in self.gui_structure.list_of_pages]

        self.verticalSpacer = QtW.QSpacerItem(20, 40, QtW.QSizePolicy.Minimum, QtW.QSizePolicy.Expanding)
        self.vertical_layout_menu.addItem(self.verticalSpacer)

        self.import_functions: dict[str, Callable[[str | Path], JsonDict]] = {
            globs.FILE_EXTENSION: normal_import,
            f"{globs.FILE_EXTENSION}BackUp": normal_import,
        }
        self.export_functions: dict[str, Callable[[str | Path, JsonDict], None]] = {
            globs.FILE_EXTENSION: normal_export,
            f"{globs.FILE_EXTENSION}BackUp": normal_export,
        }
        self.version_import_functions: dict[str, Callable[[JsonDict], JsonDict]] = {}

        # set app and dialog
        self.dia, self.app = dialog, app
        # init pop up dialog
        self.dialog: QtW.QInputDialog | None = None
        # init variables of class
        # allow checking of changes
        self.checking: bool = False
        # create backup path in home documents directory
        self.default_path: Path = Path(Path.home(), f"Documents/{globs.GUI_NAME}")
        self.backup_file: Path = Path(self.default_path, self._backup_filename)
        # check if backup folder exits and otherwise create it
        makedirs(dirname(self.backup_file), exist_ok=True)
        makedirs(dirname(self.default_path), exist_ok=True)
        for idx, (name, icon, short_cut) in enumerate(zip(self.translations.languages, self.translations.icon, self.translations.short_cut)):
            self._create_action_language(idx, name, icon, short_cut)
        # add languages to combo box
        self.gui_structure.option_language.widget.addItems(self.translations.languages)
        self.fileImport = None  # init import file
        self.filename: tuple = MainWindow.filename_default  # filename of stored inputs
        self.list_widget_scenario.clear()  # reset list widget with stored scenarios
        self.changedFile: bool = False  # set change file variable to false
        self.ax: list = []  # axes of figure
        self.threads: list[CalcProblem] = []  # list of calculation threads
        self.saving_threads: list[SavingThread] = []
        CalcProblem.role = MainWindow.role
        self.size_b = QtC.QSize(self.icon_size_large, self.icon_size_large)  # size of big logo on push button
        self.size_s = QtC.QSize(self.icon_size_small, self.icon_size_small)  # size of small logo on push button
        self.size_push_b = QtC.QSize(self.button_width_large, self.button_height)  # size of big push button
        self.size_push_s = QtC.QSize(self.button_width_small, self.button_height)  # size of small push button
        # init links from buttons to functions
        self.set_links()
        # set event filter for push button sizing
        self.set_event_filter()
        # load backup data
        self.load_backup()
        # reset push button size
        self.check_page_button_layout(False)
        # set start page to general page
        self.gui_structure.list_of_pages[0].button.click()

        self.last_idx = 0

        [option.init_links() for option, _ in self.gui_structure.list_of_options]

        globs.LOGGER.info(self.translations.tool_imported[self.gui_structure.option_language.get_value()[0]])
        # allow checking of changes
        self.checking: bool = True

        # set the correct graph layout
        globs.set_graph_layout()

        self.display_results()

        # set started to True
        # this is so that no changes are made when the file is opening
        self.gui_structure.started = True
        self.gui_structure.loaded = True

    def activate_load_as_new_scenarios(self) -> None:
        """
        activates the possibility to load files as new scenarios and append them to the current scenario list
        Returns
        -------
            None
        """
        self.menu_file.addAction(self.action_open_add)
        self.tool_bar.addAction(self.action_open_add)

    def resizeEvent(self, event: QtG.QResizeEvent) -> None:
        """
        update push buttons sizes

        Parameters
        ----------
        event: QtG.QResizeEvent

        Returns
        -------
            None
        """

        height = self.dia.size().height()
        if (len(self.gui_structure.list_of_pages) + 1) * (self.button_height + 6) > height * 0.7:
            height = max(
                int((height * 0.7 - 6 * len(self.gui_structure.list_of_pages)) / (len(self.gui_structure.list_of_pages) + 1)), self.icon_size_small + 5
            )
            # small push button
            self.size_b = QtC.QSize(
                min(self.icon_size_large, max(int(height / self.button_height * self.icon_size_large), self.size_s.height())),
                min(self.icon_size_large, max(int(height / self.button_height * self.icon_size_large), self.size_s.height())),
            )
        else:
            self.size_b = QtC.QSize(self.icon_size_large, self.icon_size_large)
        self.check_page_button_layout(False)
        QtW.QMainWindow.resizeEvent(self.dia, event)

    def add_other_import_function(self, file_extension: str, func: Callable[[str | Path], JsonDict]):
        """
        adds an import behaviour for a different file type.
        Parameters
        ----------
        file_extension: str
            file type like (*.csv)
        func: Callable[[str | Path], JsonDict]
            function which get the path to the file as input and creates a dict of results like the json format does.

        Returns
        -------
            None
        """
        self.import_functions[file_extension.replace(".", "")] = func

    def add_other_version_import_function(self, version: str, func: Callable[[JsonDict], JsonDict]):
        """
        adds an import behaviour for a previous version of the gui.
        Parameters
        ----------
        version: str
            version for which the behaviour is added
        func: Callable[[str | Path], JsonDict]
            function which get the path to the file as input and creates a dict of results like the json format does.

        Returns
        -------
            None
        """
        self.version_import_functions[version.replace("v", "").replace("V", "")] = func

    def add_other_export_function(self, file_extension: str, func: Callable[[str | Path, JsonDict], None]):
        """
        adds an export behaviour for a different file type.
        Parameters
        ----------
        file_extension: str
            file type like (*.csv)
        func: Callable[[str | Path, JsonDict], None]
            function which get the path to the file and the json dict as input and creates and saves the new file.

        Returns
        -------
            None
        """
        self.export_functions[file_extension] = func

    @property
    def list_ds(self) -> list[DataStorage]:
        return [self.list_widget_scenario.item(idx).data(MainWindow.role) for idx in range(self.list_widget_scenario.count())]

    def _create_action_language(self, idx: int, name: str, icon_name: str, short_cut: str) -> None:
        """
        This function creates an action for a specific language with name name and icon icon_name
        and couples a shortcut to this action. The action is added to the menuLanguage afterwards.

        Parameters
        ----------
        idx : int
            Index of the language in the language list
        name : str
            Name of the language
        icon_name : str
            Name of the icon
        short_cut : str
            Shortcut linked to this language

        Returns
        -------
        None
        """
        action = QtG.QAction(self.central_widget)
        icon = QtG.QIcon()
        icon.addFile(f"{globs.FOLDER}/icons/{icon_name}", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)
        action.setIcon(icon)
        self.menu_language.addAction(action)
        action.setText(name)
        action.setShortcut(short_cut)
        action.triggered.connect(ft_partial(self.gui_structure.option_language.widget.setCurrentIndex, idx))

    def set_event_filter(self) -> None:
        """
        This function sets the event filter for the page buttons so it can be detected when there is a
        mouse over event.

        Returns
        -------
        None
        """
        for page in self.gui_structure.list_of_pages:
            page.button.installEventFilter(self)
            page.label_gap.installEventFilter(self)

    def set_links(self) -> None:
        """
        This function connects all the buttons to their relevant actions.
        All interactions between front and back-end are implemented here.

        Returns
        -------
        None
        """

        setting_options = [
            (opt_cat, name)
            for category in self.gui_structure.page_settings.list_categories
            for opt_cat in category.list_of_options
            if isinstance(opt_cat, Option)
            for opt_glob, name in self.gui_structure.list_of_options
            if opt_cat == opt_glob
        ]
        for option, _ in [
            (opt, name) for opt, name in self.gui_structure.list_of_options if not isinstance(opt, FigureOption) and (opt, name) not in setting_options
        ]:
            option.change_event(self.change)
        for option, _ in [(opt, name) for opt, name in self.gui_structure.list_of_options if isinstance(opt, FigureOption)]:
            option.change_event(self.change_figure_option)
        for option, _ in [(opt, name) for opt, name in self.gui_structure.list_of_result_exports]:
            option.change_event(ft_partial(self.export_results, option))
        for option, _ in self.gui_structure.list_of_aims:
            option.change_event(self.change)

        for option, name in setting_options:
            option.change_event(ft_partial(self._change_settings_in_all_data_storages, name))

        self.gui_structure.option_language.change_event(self.change_language)
        self.gui_structure.option_font_size.change_event(self.change_font_size)
        self.gui_structure.page_result.button.clicked.connect(self.display_results)
        self.action_add_scenario.triggered.connect(self.add_scenario)
        self.action_update_scenario.triggered.connect(self.save_scenario)
        self.action_delete_scenario.triggered.connect(self.delete_scenario)
        self.action_start_multiple.triggered.connect(self.start_multiple_scenarios_calculation)
        self.action_start_single.triggered.connect(self.start_current_scenario_calculation)
        self.action_save.triggered.connect(self.fun_save)
        self.action_save_as.triggered.connect(self.fun_save_as)
        self.action_open.triggered.connect(self.fun_load)
        self.action_open_add.triggered.connect(self.load_add_scenarios)
        self.action_new.triggered.connect(self.fun_new)
        self.action_rename_scenario.triggered.connect(self.fun_rename_scenario)
        self.list_widget_scenario.setDragDropMode(QtW.QAbstractItemView.InternalMove)
        # self.list_widget_scenario.model().rowsMoved.connect(self.fun_move_scenario)
        self.list_widget_scenario.currentItemChanged.connect(self.scenario_is_changed)
        self.list_widget_scenario.itemSelectionChanged.connect(self._always_scenario_selected)
        self.gui_structure.option_auto_saving.change_event(self.change_auto_saving)
        self.dia.closeEvent = self.closeEvent
        self.dia.resizeEvent = self.resizeEvent

    def change_auto_saving(self):
        if self.gui_structure.option_auto_saving.get_value() == 1:
            self.push_button_save_scenario.hide()
            return
        self.push_button_save_scenario.show()

    def change_font_size(self):
        size = self.gui_structure.option_font_size.get_value()
        globs.FONT_SIZE = size
        rcParams.update({"font.size": size})
        self.gui_structure.change_font_size_2(size)
        change_font_size(self.push_button_save_scenario, size)
        change_font_size(self.push_button_add_scenario, size)
        change_font_size(self.push_button_delete_scenario, size)
        change_font_size(self.button_rename_scenario, size)
        change_font_size(self.push_button_cancel, size)
        change_font_size(self.push_button_start_single, size)
        change_font_size(self.push_button_start_multiple, size)
        change_font_size(self.menu_scenario, size)
        change_font_size(self.menu_calculation, size)
        change_font_size(self.menu_file, size)
        change_font_size(self.menu_settings, size)
        change_font_size(self.menu_language, size)
        change_font_size(self.menubar, size)
        change_font_size(self.list_widget_scenario, size)
        change_font_size(self.status_bar.label, size)
        change_font_size(self.progress_bar, size)
        change_font_size(self.label_status, size)
        self.remove_previous_calculated_results()

    def export_results(self, result_export: ResultExport):
        filename: tuple = QtW.QFileDialog.getSaveFileName(
            self.central_widget,
            caption=result_export.caption,
            filter=f".{result_export.file_extension} (*.{result_export.file_extension})",
            dir=str(self.default_path),
        )
        d_s = self.list_widget_scenario.currentItem().data(MainWindow.role)
        getattr(d_s.results, result_export.export_function)(filename[0])

    def change_figure_option(self):
        d_s = self.list_widget_scenario.currentItem().data(MainWindow.role)
        for option, name in [(opt, name) for opt, name in self.gui_structure.list_of_options if isinstance(opt, FigureOption)]:
            setattr(d_s, name, option.get_value())
        self.remove_previous_calculated_results()

    def remove_previous_calculated_results(self):
        """
        This function removes previously calculated results by removing the results attribute
        and closing all the figures in the DataStorage.

        Returns
        -------
        None
        """
        if self.list_widget_scenario.count() < 1:
            return
        ds = self.list_widget_scenario.currentItem().data(MainWindow.role)
        if ds.results is None:
            return
        ds.close_figures()
        # update figures
        self.display_results()

    def check_page_button_layout(self, mouse_over: bool) -> None:
        """
        This function checks if the layout of the page button should be changed.
        When the mouse_over is True, the page button is expanded to include text and icon.
        When mouse_over is False, the page button is again 'closed'.

        Parameters
        ----------
        mouse_over : bool
            True if the mouse is over a PushButton and it should be expanded

        Returns
        -------
        None
        """
        # if Mouse is over PushButton change size to big otherwise to small
        if mouse_over:
            for page in self.gui_structure.list_of_pages:
                self.change_page_button_layout(page.button, True, page.button_name)
            return
        for page in self.gui_structure.list_of_pages:
            self.change_page_button_layout(page.button)

    def change_page_button_layout(self, button: QtW.QPushButton, big: bool = False, name: str = "") -> None:
        """
        This function changes the layout of the page button, by adding/removing the text and icon.

        Parameters
        ----------
        button : QtW.QPushButton
            Button for which the layout has to be changed
        big : bool
            True if the expanded version of the button is needed, False otherwise
        name : str
            Name of the icon for the relevant button

        Returns
        -------
        None
        """
        button.setText(name)  # set name to button
        # size big or small QPushButton depending on input
        if big:
            button.setIconSize(self.size_s)
            button.setMaximumSize(self.size_push_b)
            button.setMinimumSize(self.size_push_b.width(), self.size_s.height() + 5)
            button.resize(self.size_push_b)
            button.setSizePolicy(QtW.QSizePolicy.Fixed, QtW.QSizePolicy.Expanding)
            return
        button.setIconSize(self.size_b)
        # icon: QtG.QIcon = button.icon()
        # icon.si
        button.setMaximumSize(self.size_push_s)
        button.setMinimumSize(self.size_s.height() + 5, self.size_s.height() + 5)
        button.setSizePolicy(QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Expanding)
        # button.setMinimumSize(self.size_push_s)
        button.resize(self.size_push_s)

    def change(self) -> None:
        """
        This function checks if there are changes to a scenario or a file save happened.
        If there were changes, an * is added to the current scenario.
        This function is only active when self.started is True (this is the case when the application is running)
        and self.checking is True (this can temporarily be disabled by some other function).

        Returns
        -------
        None
        """
        # return if not yet started or return if checking is not allowed
        if not self.gui_structure.started or not self.checking:
            return
        self.check_buttons()
        # if changed File is not already True set it to True and update window title
        if self.changedFile is False:
            self.changedFile: bool = True
            self.change_window_title()
        # get current index of scenario
        item = self.list_widget_scenario.currentItem()
        if item is None:
            return
        # remove results object
        item.data(MainWindow.role).close_figures()
        item.data(MainWindow.role).results = None
        # abort here if autosave scenarios is used
        if self.gui_structure.option_auto_saving.get_value() == 1:
            return
        # get text string of current scenario
        text: str = self.list_widget_scenario.currentItem().text()
        # create current data storage
        d_s: DataStorage = DataStorage(self.gui_structure)
        # check if current data storage is equal to the previous one then delete the *
        if d_s == item.data(MainWindow.role):
            if text[-1] != "*":
                return
            item.setText(text[:-1])
            return
        # if scenario is already marked as changed return
        if text[-1] == "*":
            return
        # else add * to current item string
        item.setText(f"{text}*") if self.gui_structure.started else None

    def check_buttons(self):
        try:
            not_running = self.list_widget_scenario.currentItem() not in [thread.item for thread in self.threads]
        except RuntimeError:  # pragma: no cover
            not_running = True
        if self.check_values() and not_running:
            self.push_button_start_multiple.setEnabled(True)
            self.push_button_start_single.setEnabled(True)
            self.push_button_save_scenario.setEnabled(True)
        else:
            self.push_button_start_multiple.setEnabled(False)
            self.push_button_start_single.setEnabled(False)
            self.push_button_save_scenario.setEnabled(False)
        if self.check_values():
            self.list_widget_scenario.setEnabled(True)
            self.push_button_add_scenario.setEnabled(True)
        else:
            self.list_widget_scenario.setEnabled(False)
            self.push_button_add_scenario.setEnabled(False)

    def scenario_is_changed(self, new_row_item: QtW.QListWidgetItem, old_row_item: QtW.QListWidgetItem) -> None:
        """
        This function handles the changing of scenarios.
        If the auto-save ButtonBox is set to auto-save, the previous scenario is changed an the new item is selected.
        If not, a messagebox is shown to ask if the 'old' scenario should be saved.

        Parameters
        ----------
        new_row_item : QtW.QListWidgetItem
            New selected item in the scenario listbox
        old_row_item : QtW.QListWidgetItem
            Old selected item in the scenario listbox

        Returns
        -------
        None
        """
        # return if not checking
        if new_row_item is None or not self.checking:
            return

        self.check_buttons()
        # if no old item is selected do nothing and return
        if old_row_item is None:
            # change entries to new scenario values
            self.change_scenario(self.list_widget_scenario.row(new_row_item))
            return

        if new_row_item.text() == old_row_item.text():
            return

        def return_2_old_item():
            # change item to old item by thread, because I have not found a direct way which is not lost after return
            d_s = DataStorage(self.gui_structure)

            def returning():
                self.list_widget_scenario.blockSignals(True)
                self.checking = False
                self.list_widget_scenario.setCurrentItem(old_row_item)
                # set values of selected Datastorage
                d_s.set_values(self.gui_structure)
                self.checking = True
                self.list_widget_scenario.blockSignals(False)

            QtC.QTimer.singleShot(10, returning)

        # check if the auto saving should be performed and then save the last selected scenario
        if self.gui_structure.option_auto_saving.get_value() == 1:
            self.check_values()
            # save old scenario
            if (
                self.list_widget_scenario.count() - 1 >= self.list_widget_scenario.row(old_row_item)
                and DataStorage(self.gui_structure) != old_row_item.data(MainWindow.role)
                and self.push_button_save_scenario.isEnabled()
            ):
                old_row_item.data(MainWindow.role).close_figures()
                old_row_item.setData(MainWindow.role, DataStorage(self.gui_structure))
            # update backup fileImport
            self.auto_save()
            # change values to new scenario values
            self.change_scenario(self.list_widget_scenario.row(new_row_item))
            # abort function
            return
        # get test of old scenario (item)
        text = old_row_item.text()
        # check if the old scenario is unsaved then create message box
        if text[-1] == "*":
            # create message box
            self.dialog: QtW.QMessageBox = QtW.QMessageBox(self.dia)
            set_default_font(self.dialog)
            # set Icon to question mark icon
            self.dialog.setIcon(QtW.QMessageBox.Question)
            # set label text to leave scenario text depending on language selected
            self.dialog.setText(self.translations.label_LeaveScenarioText[self.gui_structure.option_language.get_value()[0]])
            # set window text to  leave scenario text depending on language selected
            self.dialog.setWindowTitle(self.translations.label_CancelTitle[self.gui_structure.option_language.get_value()[0]])
            # set standard buttons to save, close and cancel
            self.dialog.setStandardButtons(QtW.QMessageBox.Save | QtW.QMessageBox.Close | QtW.QMessageBox.Cancel)
            # get save, close and cancel button
            button_s = self.dialog.button(QtW.QMessageBox.Save)
            button_cl = self.dialog.button(QtW.QMessageBox.Close)
            button_ca = self.dialog.button(QtW.QMessageBox.Cancel)
            # set save, close and cancel button text depending on language selected
            button_s.setText(f"{self.translations.push_button_save_scenario[self.gui_structure.option_language.get_value()[0]]} ")
            button_cl.setText(f"{self.translations.label_LeaveScenario[self.gui_structure.option_language.get_value()[0]]} ")
            button_ca.setText(f"{self.translations.label_StayScenario[self.gui_structure.option_language.get_value()[0]]} ")
            # set  save, close and cancel button icon
            self.set_push_button_icon(button_s, "Save_Inv")
            self.set_push_button_icon(button_cl, "Exit")
            self.set_push_button_icon(button_ca, "Abort")
            [set_default_font(button) for button in self.dialog.findChildren(QtW.QPushButton)]
            # execute message box and save response
            reply = self.dialog.exec()
            # check if closing should be canceled
            if reply == QtW.QMessageBox.Cancel:
                return_2_old_item()
                return
            # save scenario if wanted
            if reply == QtW.QMessageBox.Save:  # pragma: no cover
                old_row_item.setData(MainWindow.role, DataStorage(self.gui_structure))
            # remove * symbol
            old_row_item.setText(text[:-1])
        # change entries to new scenario values
        self.change_scenario(self.list_widget_scenario.row(new_row_item))
        return

    @staticmethod
    def set_push_button_icon(button: QtW.QPushButton, icon_name: str) -> None:
        """
        This function sets the icon in the QPushButton.

        Parameters
        ----------
        button : QtW.QPushButton
            Button to which the icon should be set
        icon_name : str
            Icon name

        Returns
        -------
        None
        """
        icon = QtG.QIcon()  # create icon class
        # add pixmap to icon
        icon.addPixmap(
            QtG.QPixmap(f"{globs.FOLDER}/icons/{icon_name}.svg"),
            QtG.QIcon.Normal,
            QtG.QIcon.Off,
        )
        button.setIcon(icon)  # set icon to button

    def set_name(self, name: str) -> str:
        """
        set the text of the item and checks for the appearens in the current scenario names
        Parameters
        ----------
        name: str
            scenario name

        Returns
        -------
            str
        """
        # sets the name of the current scenario to text
        if name in [self.list_widget_scenario.item(x).text().split("*")[0] for x in range(self.list_widget_scenario.count())]:
            name += "(2)"
        return name

    def fun_rename_scenario(self, name: str = "") -> None:
        """
        Function to rename the current scenario with a dialog box to ask for a new name

        Parameters
        ----------
        name : str
            Name of the scenario (only for testing purposes

        Returns
        -------
        None
        """
        # get current item
        item = self.list_widget_scenario.currentItem()
        # return if no scenarios exits
        if item is None:
            return

        # get first item if no one is selected
        item = self.list_widget_scenario.item(0) if item is None else item
        if name:
            item.setText(self.set_name(name)) if name else None
            return

        # create dialog box to ask for a new name
        self.dialog = QtW.QInputDialog(self.dia)
        set_default_font(self.dialog)
        self.dialog.setTextValue(item.text())
        self.dialog.setWindowTitle(self.translations.label_new_scenario[self.gui_structure.option_language.get_value()[0]])
        self.dialog.setLabelText(f"{self.translations.new_name[self.gui_structure.option_language.get_value()[0]]}{item.text()}")
        self.dialog.setOkButtonText(self.translations.label_okay[self.gui_structure.option_language.get_value()[0]])  # +++
        self.dialog.setCancelButtonText(self.translations.label_abort[self.gui_structure.option_language.get_value()[0]])  # +++
        li = self.dialog.findChildren(QtW.QPushButton)
        self.set_push_button_icon(li[0], "Okay")
        self.set_push_button_icon(li[1], "Abort")
        [set_default_font(button) for button in li]
        # set new name if the dialog is not canceled and the text is not None
        if self.dialog.exec() == QtW.QDialog.Accepted:
            name = self.dialog.textValue()
            item.setText(self.set_name(name)) if name else None

        self.dialog = None

    def check_results(self) -> None:
        """
        This function checks if there are results and if so, it will display them.
        It checks this by checking if there exists a results attribute in the datastorage object
        that differs from None.

        Returns
        -------
        None
        """
        # hide results buttons if no results where found
        if (
            any((self.list_widget_scenario.item(i).data(MainWindow.role).results is None) for i in range(self.list_widget_scenario.count()))
            or self.list_widget_scenario.count() < 1
        ):
            # self.gui_structure.function_save_results.hide()
            self.gui_structure.list_of_pages[0].button.click()
            return
        # display results otherwise
        self.display_results()

    def change_window_title(self) -> None:
        """
        This function changes the window title to the filename and marks it with an * if unsaved changes exist

        Returns
        -------
        None
        """
        # get filename separated from path
        _, filename = MainWindow.filename_default if self.filename == MainWindow.filename_default else os_split(self.filename[0])
        # title determine new title if a filename is not empty
        title: str = "" if not filename else f' - {filename.replace(".FILE_EXTENSION", "")}'
        # create new title name
        name: str = f"{globs.GUI_NAME} v{globs.VERSION} {title}*" if self.changedFile else f"{globs.GUI_NAME} v{globs.VERSION} {title}"
        # set new title name
        self.dia.setWindowTitle(name)

    def eventFilter(self, obj: QtW.QPushButton, event) -> bool:  # noqa: N802
        """
        This function checks the mouse over event. It overwrites the eventFilter object in QObject.

        Parameters
        ----------
        obj : QtW.QPushButton
        event : event
            Event for which it is check if the mouse is entering or leaving

        Returns
        -------
        bool
            True to check if the function has worked correctly. (implemented for test cases)
        """
        if event.type() == QtC.QEvent.Enter:
            # Mouse is over the label
            self.check_page_button_layout(True)
            return True
        elif event.type() == QtC.QEvent.Leave:
            # Mouse is not over the label
            self.check_page_button_layout(False)
            return True
        return super().eventFilter(obj, event)

    def _change_settings_in_all_data_storages(self, name_of_option: str, *args) -> None:
        """
        This function makes sure that the settings are the same in all the different scenarios.

        Parameters
        ----------
        name_of_option : str
            Name of the option that has been changed
        args
            Other arguments that can be passed through

        Returns
        -------
        None
        """
        for idx in range(self.list_widget_scenario.count()):
            data = self.list_widget_scenario.item(idx).data(MainWindow.role)
            setattr(
                data,
                name_of_option,
                getattr(self.gui_structure, name_of_option).get_value(),
            )
            self.list_widget_scenario.item(idx).setData(MainWindow.role, data)

    def change_language(self) -> None:
        """
        This function changes the language on the different labels and buttons in the gui.

        Returns
        -------
        None
        """
        self.checking = False
        scenario_index: int = self.list_widget_scenario.currentRow()  # get current selected scenario
        amount: int = self.list_widget_scenario.count()  # number of scenario elements

        # check if list scenario names are not unique
        li_str_match: list[bool] = [
            self.list_widget_scenario.item(idx).text() == f"{self.translations.scenarioString[self.gui_structure.option_language.get_value()[0]]}: {idx + 1}"
            for idx in range(amount)
        ]
        # update all label, pushButtons, action and Menu names
        for i in [j for j in self.translations.__slots__ if hasattr(self, j)]:
            if isinstance(getattr(self, i), QtW.QMenu):
                getattr(self, i).setTitle(getattr(self.translations, i)[self.gui_structure.option_language.get_value()[0]])
                continue
            getattr(self, i).setText(getattr(self.translations, i)[self.gui_structure.option_language.get_value()[0]])
        # set translation of toolbox items
        self.gui_structure.translate(self.gui_structure.option_language.get_value()[0], self.translations)
        for idx, name in enumerate(self.translations.languages):
            self.gui_structure.option_language.widget.setItemText(idx, name)
        # set small PushButtons
        self.check_page_button_layout(False)
        # replace scenario names if they are not unique
        scenarios: list = [
            f"{self.translations.scenarioString[self.gui_structure.option_language.get_value()[0]]}: {i}"
            if li_str_match[i - 1]
            else self.list_widget_scenario.item(i - 1).text()
            for i in range(1, amount + 1)
        ]
        # clear list widget with scenario and write new ones
        for idx, name in enumerate(scenarios):
            self.list_widget_scenario.item(idx).setText(name)
        # select current scenario
        self.list_widget_scenario.setCurrentRow(scenario_index) if scenario_index >= 0 else None
        self.checking = True

    def delete_backup(self):
        """
        This function deletes the backup file link (not the actual backup file) if it exists.

        Returns
        -------
        None
        """
        if exists(self.backup_file):  # pragma: no cover
            remove(self.backup_file)

    def load_backup(self) -> None:
        """
        This function tries to open the backup file and load its values.

        Returns
        -------
        None
        """
        # try to open backup file if it exits
        if exists(self.backup_file):
            self._load_from_data(self.backup_file)
            # change language to english if no change has happened
            self.checking = False
            if self.gui_structure.option_language.get_value()[0] == 0:
                self.change_language()
            self.checking = True
            return
        # change language to english
        self.change_language()
        # show message that no backup file is found
        globs.LOGGER.error(self.translations.no_backup_file[self.gui_structure.option_language.get_value()[0]])

    def auto_save(self) -> None:
        """
        This function automatically saves data in the backup file.

        Returns
        -------
        None
        """
        # append scenario if no scenario is in list
        if self.list_widget_scenario.count() < 1:
            self.add_scenario()

        func = ft_partial(self._save_to_data, self.backup_file)
        self.saving_threads.append(SavingThread(datetime.datetime.now(), func))
        self._saving_threads_update()

    def _saving_threads_update(self):
        if len(self.saving_threads) < 1:
            return
        thread = self.saving_threads[0]
        if thread.calculated:
            thread.terminate()
            self.saving_threads.remove(thread)
            self._saving_threads_update()
            return
        if thread.isRunning():  # pragma: no cover
            return
        thread.any_signal.connect(self._saving_threads_update)
        thread.start() if not MainWindow.TEST_MODE else None

    def _load_from_data(self, location: str | Path, append: bool = False) -> None:
        """
        This function loads the data from a JSON formatted file.

        Parameters
        ----------
        location : str
            Location of the data file

        Returns
        -------
        None
        """
        file_extension = splitext(location)[1].replace(".", "")
        func = self.import_functions[file_extension]
        try:
            saving = func(location)
        except FileNotFoundError:
            globs.LOGGER.error(self.translations.no_file_selected[self.gui_structure.option_language.get_value()[0]])
            return
        if saving["version"] in self.version_import_functions:
            saving = self.version_import_functions[saving["version"]](saving)
        # set and change the window title
        if not append:
            self.filename = tuple(saving["filename"])
            self.change_window_title()
            self.list_widget_scenario.clear()
        else:
            self.changedFile: bool = True
            self.change_window_title()
        # write data to variables
        for _idx, (val, results, name) in enumerate(zip(saving["values"], saving["results"], saving["names"])):
            d_s = DataStorage(self.gui_structure)
            d_s.from_dict(val)
            d_s.results = None if results is None else self.result_creating_class.from_dict(results)
            item = QtW.QListWidgetItem(self.set_name(name))
            item.setData(MainWindow.role, d_s)
            self.list_widget_scenario.addItem(item)

        self.list_widget_scenario.setCurrentRow(0)
        ds = self.list_widget_scenario.item(0).data(self.role)
        if ds != DataStorage(self.gui_structure):
            self.checking = False
            ds.set_values(self.gui_structure)
            self.checking = True
        self.check_results()

    def _save_to_data(self, location: str | Path) -> None:
        """
        This function saves the gui data to a json formatted file.

        Parameters
        ----------
        location : str
            Location of the data file.

        Returns
        -------
        None
        """
        # create list of all scenario names
        scenario_names = [self.list_widget_scenario.item(idx).text() for idx in range(self.list_widget_scenario.count())]
        # create saving dict
        list_ds = [self.list_widget_scenario.item(idx).data(MainWindow.role) for idx in range(self.list_widget_scenario.count())]
        saving: JsonDict = {
            "filename": self.filename,
            "names": scenario_names,
            "version": globs.VERSION,
            "values": [d_s.to_dict() for d_s in list_ds],
            "results": [d_s.results.to_dict() if d_s.results is not None else None for d_s in list_ds],
        }

        file_extension = splitext(location)[1].replace(".", "")
        try:
            self.export_functions[file_extension](location, saving)
        except FileNotFoundError:
            globs.LOGGER.error(self.translations.no_file_selected[self.gui_structure.option_language.get_value()[0]])
        except PermissionError:  # pragma: no cover
            globs.LOGGER.error("PermissionError")

    def load_add_scenarios(self) -> None:
        """
        This function sets the filename by opening a QFileDialog box.
        Afterwards, it runs fun_load_known_filename() to open this file.

        Returns
        -------
        None
        """
        # open interface and get file name
        filename = QtW.QFileDialog.getOpenFileName(
            self.central_widget,
            caption=self.translations.choose_load[self.gui_structure.option_language.get_value()[0]],
            filter=";;".join(
                extension
                for extension in [f"{globs.FILE_EXTENSION} (*.{globs.FILE_EXTENSION})"]
                + [f"{extension} (*.{extension})" for extension in list(self.import_functions.keys())[2:]]
            ),
            dir=str(self.default_path),
        )
        # break function if no file is selected
        if filename == MainWindow.filename_default or not filename[0]:
            return
        # deactivate checking
        self.checking: bool = False
        self.gui_structure.loaded = False
        # open file and set data
        self._load_from_data(filename[0], append=True)
        # activate checking
        self.checking: bool = True
        self.gui_structure.loaded = True

    def fun_load(self) -> None:
        """
        This function sets the filename by opening a QFileDialog box.
        Afterwards, it runs fun_load_known_filename() to open this file.

        Returns
        -------
        None
        """
        # open interface and get file name
        filename = QtW.QFileDialog.getOpenFileName(
            self.central_widget,
            caption=self.translations.choose_load[self.gui_structure.option_language.get_value()[0]],
            filter=";;".join(
                extension
                for extension in [f"{globs.FILE_EXTENSION} (*.{globs.FILE_EXTENSION})"]
                + [f"{extension} (*.{extension})" for extension in list(self.import_functions.keys())[2:]]
            ),
            dir=str(self.default_path),
        )
        # break function if no file is selected
        if filename == MainWindow.filename_default or not filename[0]:
            return
        self.filename = filename
        # load selected data
        self.fun_load_known_filename()

    def fun_load_known_filename(self) -> None:
        """
        This function loads a previously stored project based on the self.filename attribute.
        This attribute is set by the function fun_load().
        When no such file exists, a message is printed in the status bar.

        Returns
        -------
        None
        """
        # deactivate checking
        self.checking: bool = False
        self.gui_structure.loaded = False
        # open file and set data
        self._load_from_data(self.filename[0])
        # activate checking
        self.checking: bool = True
        self.gui_structure.loaded = True

    def fun_save_as(self) -> None:
        """
        This function sets the filename to a default value and calls the fun_save() function.

        Returns
        -------
        None
        """
        # reset filename because then the funSave function ask for a new filename
        filename: tuple = QtW.QFileDialog.getSaveFileName(
            self.central_widget,
            caption=self.translations.Save[self.gui_structure.option_language.get_value()[0]],
            filter=";;".join(
                extension
                for extension in [f"{globs.FILE_EXTENSION} (*.{globs.FILE_EXTENSION})"]
                + [f"{extension} (*.{extension})" for extension in list(self.export_functions.keys())[2:]]
            ),
            dir=str(self.default_path),
        )
        # break function if no file is selected
        if filename == MainWindow.filename_default or not filename[0]:
            return
        self.filename = filename if splitext(filename[0])[1].replace(".", "") == globs.FILE_EXTENSION else self.filename
        self.fun_save(filename)  # save data under a new filename

    def fun_save(self, filename: tuple[str, str] | None = None) -> bool:
        """
        This function saves all the scenarios in a JSON formatted *.{FILE_EXTENSION} file.

        Parameters
        -------
        filename: tuple[str, str] | None
            name of file

        Returns
        -------
        bool
            True if the saving was successful.
        """
        # ask for pickle file if the filename is still the default
        logging.info(f"{filename}, {MainWindow.filename_default}: {self.filename}")
        if not isinstance(filename, tuple):
            if self.filename == MainWindow.filename_default:
                self.fun_save_as()
                return True
            else:
                filename = self.filename

        self.change_window_title() if self.filename == filename else None
        # save scenarios
        self.save_scenario()
        # update backup file
        self.auto_save()
        # try to store the data in the pickle file
        func = ft_partial(self._save_to_data, filename[0])
        self.saving_threads.append(SavingThread(datetime.datetime.now(), func))
        self._saving_threads_update()
        # deactivate changed file * from window title
        self.changedFile: bool = False
        self.change_window_title()
        # return true because everything was successful
        return True

    def fun_new(self) -> None:
        """
        This function creates a new project and resets the GUI.

        Returns
        -------
        None
        """
        self.filename: tuple = MainWindow.filename_default  # reset filename
        if self.fun_save():  # get and save filename
            self.list_widget_scenario.clear()  # clear list widget with scenario list
            self.display_results()  # clear the results page

    def _always_scenario_selected(self) -> None:
        """
        This function makes sure there is always a scenario selected.
        If no scenario is selected, the last scenario is selected.

        Returns
        -------
        None
        """
        if not self.list_widget_scenario.selectedItems():
            self.list_widget_scenario.setCurrentRow(self.last_idx)
        else:
            self.last_idx = self.list_widget_scenario.currentRow()

    def change_scenario(self, idx: int) -> None:
        """
        Updates the gui to the correct data from the datastorage with the selected index idx.

        Parameters
        ----------
        idx : int
            Index of the selected scenario

        Returns
        -------
        None
        """
        # if i no scenario is selected (idx < 0) or no scenario exists break function
        item = self.list_widget_scenario.item(idx)
        # get selected Datastorage from list
        d_s: DataStorage = item.data(MainWindow.role)
        # deactivate checking for changes
        self.checking: bool = False
        # set values of selected Datastorage
        d_s.set_values(self.gui_structure)
        # refresh results if results page is selected
        self.display_results() if self.stacked_widget.currentWidget() == self.gui_structure.page_result.page else None
        # activate checking for changed
        self.checking: bool = True

    def check_values(self) -> bool:
        """
        This function checks if all the options in the gui are given correct values.
        If not, it will print an error message on the status bar.

        Returns
        -------
        None
        """
        if not all(option.check_value() for option, _ in self.gui_structure.list_of_options):
            for option, _ in self.gui_structure.list_of_options:
                if not option.check_value():
                    globs.LOGGER.info(f"Wrong value in option with label: {option.label_text[0]}")
                    return False
        return True

    def save_scenario(self) -> bool:
        """
        This function saves the current scenario in the backup.

        Returns
        -------
        None
        """
        if not self.check_values():
            return False
        # get selected scenario index
        item = self.list_widget_scenario.currentItem()
        # if no scenario exists create a new one else save DataStorage with new inputs in list of scenarios
        if item is None:
            self.add_scenario()
            item = self.list_widget_scenario.currentItem()
        elif item.data(MainWindow.role).results is None:  # do not overwrite any results
            item.data(MainWindow.role).close_figures()
            item.setData(MainWindow.role, DataStorage(self.gui_structure))
        # remove * from scenario if not Auto save is checked and if the last char is a *
        if self.gui_structure.option_auto_saving.get_value() != 1:
            text = item.text()
            if text[-1] == "*":
                item.setText(text[:-1])
        # create auto backup
        self.auto_save()
        return True

    def delete_scenario(self) -> None:
        """
        This function deletes the selected scenario and selects the scenario above it.

        Returns
        -------
        None
        """
        if self.list_widget_scenario.count() < 2:  # noqa: PLR2004
            return
        # get current scenario index
        item = self.list_widget_scenario.currentItem()
        # check if it is not scenarios exists and not the last one is selected (The last one can not be deleted)
        item.data(MainWindow.role).close_figures()
        idx = self.list_widget_scenario.row(item)
        # delete scenario form list widget
        self.list_widget_scenario.takeItem(idx)
        # select previous scenario then the deleted one but at least the first one
        self.list_widget_scenario.setCurrentRow(max(idx - 1, 0))
        self.change_scenario(max(idx - 1, 0))

    def add_scenario(self) -> None:
        """
        Function to add a scenario.

        Returns
        -------
        None
        """
        # get current number of scenario but at least 0
        number: int = self.list_widget_scenario.count()
        # add new scenario name and item to list widget
        string = f"{self.translations.scenarioString[self.gui_structure.option_language.get_value()[0]]}: {number + 1}"
        if string in [self.list_widget_scenario.item(x).text().split("*")[0] for x in range(number)]:
            string += "(2)"
        # select new list item
        item = QtW.QListWidgetItem(string)
        item.setData(MainWindow.role, DataStorage(self.gui_structure))
        self.list_widget_scenario.addItem(item)
        self.list_widget_scenario.setCurrentRow(number)
        # run change function to mark unsaved inputs
        self.change()

    def update_bar(self, val: int) -> None:
        """
        This function updates the status bar or hides them if it is no longer needed.
        It displays the percentage of calculated scenarios.

        Parameters
        ----------
        val : int
            Number of successfully calculated scenarios
        opt_start : bool
            True if the calculation is started and the progressbar should be shown

        Returns
        -------
        None
        """
        # show label and progress bar if calculation started otherwise hide them
        self.status_bar_progress_bar.show()
        # calculate percentage of calculated scenario
        val = val / max(len(self.threads), 1)
        # set percentage to progress bar
        self.progress_bar.setValue(round(val * 100))
        # hide labels and progressBar if all scenarios are calculated
        if all(thread.calculated for thread in self.threads):
            self.threads = []
            self.progress_bar.setValue(100)
            self.status_bar_progress_bar.hide()
            # show message that calculation is finished
            globs.LOGGER.info(self.translations.Calculation_Finished[self.gui_structure.option_language.get_value()[0]])

    def thread_function(self, results: CalcProblem) -> None:
        """
        This function closes the thread of the old calculation and stores it results.
        It increments the number of calculated scenarios, and calls to update the progress bar.
        Afterwards, it starts the new thread for the following calculation.

        Parameters
        ----------
        results : Tuple[DataStorage, int]
            Tuple with the DS object of the current thread and its corresponding index

        Returns
        -------
        None
        """
        # stop finished thread
        results.terminate()
        # count number of finished calculated scenarios
        item_list = [thread.item for thread in self.threads]
        open_threads = [thread for thread in self.threads if not thread.calculated and not thread.isRunning()]
        n_closed_threads = len(self.threads) - len([thread for thread in self.threads if not thread.calculated])
        # update progress bar
        self.update_bar(n_closed_threads)
        # if number of finished is the number that has to be calculated enable buttons and actions and change page to
        # results page
        if open_threads:  # pragma: no cover
            # start new thread
            open_threads[0].start() if not MainWindow.TEST_MODE else None
            open_threads[0].any_signal.connect(self.thread_function)
            return
        # display results
        self.check_buttons()
        if self.list_widget_scenario.currentItem() in item_list:
            self.gui_structure.page_result.button.click()

    def start_multiple_scenarios_calculation(self) -> None:
        """
        This function starts the calculation of all the scenarios that do not have a results attribute in their
        DS, when check_values() is True.

        Returns
        -------
        None
        """
        if not self.check_values():
            return
        # add scenario if no list of scenarios exits else save current scenario
        self.add_scenario() if self.list_widget_scenario.count() < 1 else self.save_scenario()
        # create list of threads with scenarios that have not been calculated
        self.threads += [
            CalcProblem(
                self.list_widget_scenario.item(idx).data(MainWindow.role),
                self.list_widget_scenario.item(idx),
                data_2_results_function=self.data_2_results_function,
            )
            for idx in range(self.list_widget_scenario.count())
            if self.list_widget_scenario.item(idx).data(MainWindow.role).results is None
        ]
        # set number of to calculate scenarios
        if len(self.threads) < 1:
            return
        # disable buttons and actions to avoid two calculation at once
        self.check_buttons()
        # update progress bar
        self.update_bar(0)
        # start calculation if at least one scenario has to be calculated
        if [thread for thread in self.threads if thread.isRunning()]:  # pragma: no cover
            return
        for thread in self.threads[: self.gui_structure.option_n_threads.get_value()]:
            thread.start() if not MainWindow.TEST_MODE else None
            thread.any_signal.connect(self.thread_function)

    def start_current_scenario_calculation(self) -> None:
        """
        This function starts the calculation of the selected/current scenario, when check_values() is True.

        Returns
        -------
        None
        """
        if not self.check_values():
            return
        # add scenario if no list of scenarios exits else save current scenario
        self.add_scenario() if self.list_widget_scenario.count() < 1 else self.save_scenario() if self.list_widget_scenario.currentItem().text()[
            -1
        ] == "*" else None
        # get Datastorage of selected scenario
        ds: DataStorage = self.list_widget_scenario.currentItem().data(MainWindow.role)
        # if calculation is already done just show results
        if ds.results is not None:
            self.gui_structure.page_result.button.click()
            return
        # create list of threads with calculation to be made
        self.threads += [CalcProblem(ds, self.list_widget_scenario.currentItem(), data_2_results_function=self.data_2_results_function)]
        # disable buttons and actions to avoid two calculation at once
        self.check_buttons()
        # update progress bar
        self.update_bar(0)
        # start calculation
        if len(self.threads) == 1:
            self.threads[0].start() if not MainWindow.TEST_MODE else None
            self.threads[0].any_signal.connect(self.thread_function)

    def display_results(self) -> None:
        """
        This function displays the results (of the selected scenario) on the results page.

        Returns
        -------
        None
        """

        def update_results():
            # update so all the relevant options are shown
            check_aim_options([aim for aim, _ in self.gui_structure.list_of_aims])
            [option.show() for option, _ in self.gui_structure.list_of_options_with_dependent_results if not option.is_hidden()]

        # hide widgets if no list of scenarios exists and display not calculated text
        def hide_no_result(hide: bool = True):
            if hide or self.list_widget_scenario.currentItem().text()[-1] == "*":
                for cat in self.gui_structure.page_result.list_categories:
                    cat.hide(results=True)
                self.gui_structure.cat_no_results.show()
                self.gui_structure.text_no_result.set_text(self.translations.not_calculated[self.gui_structure.option_language.get_value()[0]])
                return
            update_results()
            for cat in self.gui_structure.page_result.list_categories:
                cat.show(results=True)
            # make sure all the results are being shown
            self.gui_structure.cat_no_results.hide()

        if self.list_widget_scenario.count() < 1:
            hide_no_result(True)
            return

        # get Datastorage of selected scenario
        ds: DataStorage = self.list_widget_scenario.currentItem().data(MainWindow.role)
        # get results of selected scenario
        results = ds.results

        # set debug message
        if ds.debug_message:
            hide_no_result(True)
            self.gui_structure.text_no_result.set_text(str(ds.debug_message))
            return

        # hide widgets if no results exists and display not calculated text
        if results is None:
            hide_no_result(True)
            return
        # no errors, so proceed with showing the results
        hide_no_result(False)
        # create figure for every ResultFigure object
        for fig_obj, fig_name in self.gui_structure.list_of_result_figures:
            if fig_obj.is_hidden():
                continue

            fig = getattr(ds, fig_name)
            if fig is None:
                globs.set_graph_layout()
                # create axes and drawing
                fig, ax_new = getattr(results, fig_obj.function_name)(**fig_obj.kwargs)
                fig_obj.replace_figure(fig)
                globs.set_graph_layout()
                # show everything
                fig_obj.show()
                fig_obj.canvas.show()
                # draw new plot
                fig.tight_layout() if fig_obj.frame.isVisible() else None
                fig_obj.canvas.draw()
                # set figure to datastorage
                setattr(ds, fig_name, fig)
                continue
            globs.set_graph_layout()
            fig_obj.replace_figure(fig)
            globs.set_graph_layout()
            # show everything
            fig_obj.show()
            fig_obj.canvas.show()
            # draw new plot
            fig.tight_layout() if fig_obj.frame.isVisible() and not(fig_obj.fig.get_tight_layout()) else None
            fig_obj.canvas.draw()

        # update result for every ResultText object
        for (
            result_text_obj,
            _,
        ) in self.gui_structure.list_of_result_texts:
            if not result_text_obj.is_hidden():
                text = results.__getattribute__(result_text_obj.var_name)  # currently only results
                if callable(text):
                    text = getattr(results, result_text_obj.var_name)()
                result_text_obj.set_text_value(text)

    def closeEvent(self, event) -> None:  # noqa: N802
        """
        This function is called when the gui is closed. It will prompt a window asking if potential changes
        need to be saved.

        Parameters
        ----------
        event
            closing event

        Returns
        -------
        None
        """
        # close app if nothing has been changed
        if not self.changedFile:
            event.accept()
            return
        # create message box
        self.dialog: QtW.QMessageBox = QtW.QMessageBox(self.dia)
        set_default_font(self.dialog)
        # set Icon to question mark icon
        self.dialog.setIcon(QtW.QMessageBox.Question)
        # set label text to cancel text depending on language selected
        self.dialog.setText(self.translations.label_CancelText[self.gui_structure.option_language.get_value()[0]])
        # set window text to cancel text depending on language selected
        self.dialog.setWindowTitle(self.translations.label_CancelTitle[self.gui_structure.option_language.get_value()[0]])
        # set standard buttons to save, close and cancel
        self.dialog.setStandardButtons(QtW.QMessageBox.Save | QtW.QMessageBox.Close | QtW.QMessageBox.Cancel)
        # get save, close and cancel button
        button_s = self.dialog.button(QtW.QMessageBox.Save)
        button_cl = self.dialog.button(QtW.QMessageBox.Close)
        button_ca = self.dialog.button(QtW.QMessageBox.Cancel)
        [set_default_font(button) for button in self.dialog.findChildren(QtW.QPushButton)]
        # set save, close and cancel button text depending on language selected
        button_s.setText(f"{self.translations.label_Save[self.gui_structure.option_language.get_value()[0]]} ")
        button_cl.setText(f"{self.translations.label_close[self.gui_structure.option_language.get_value()[0]]} ")
        button_ca.setText(f"{self.translations.label_cancel[self.gui_structure.option_language.get_value()[0]]} ")
        # set  save, close and cancel button icon
        self.set_push_button_icon(button_s, "Save_Inv")
        self.set_push_button_icon(button_cl, "Exit")
        self.set_push_button_icon(button_ca, "Abort")
        # execute message box and save response
        reply = self.dialog.exec()
        # check if closing should be canceled
        if reply == QtW.QMessageBox.Cancel:
            # cancel closing event
            event.ignore()
            return
        # check if inputs should be saved and if successfully set closing variable to true
        close: bool = self.fun_save() if reply == QtW.QMessageBox.Save else True
        # stop all calculation threads
        _ = [i.terminate() for i in self.threads]
        # close figures
        _ = [self.list_widget_scenario.item(idx).data(MainWindow.role).close_figures() for idx in range(self.list_widget_scenario.count())]
        # close window if close variable is true else not
        event.accept() if close else event.ignore()
