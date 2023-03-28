import os

import keyboard
import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as globs
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_close(qtbot):
    """
    test if the close dialog works correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """

    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(2.1)
    # set filenames
    filename_1 = f"test_1.{globs.FILE_EXTENSION}"
    # delete files if they already exists
    if os.path.exists(main_window.default_path.joinpath(filename_1)):  # pragma: no cover
        os.remove(main_window.default_path.joinpath(filename_1))

    def close():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QMessageBox):
            main_window.dialog.close()

    def cancel():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QMessageBox):
            main_window.dialog.buttons()[2].click()

    def exit_window():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QMessageBox):
            main_window.dialog.buttons()[1].click()

    def save():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QMessageBox):
            main_window.dialog.buttons()[0].click()

    QtC.QTimer.singleShot(250, close)
    main_window.close()

    QtC.QTimer.singleShot(250, cancel)
    main_window.close()

    QtC.QTimer.singleShot(250, save)
    QtC.QTimer.singleShot(270, lambda: keyboard.write(filename_1))
    QtC.QTimer.singleShot(280, lambda: keyboard.press("enter"))
    main_window.close()

    QtC.QTimer.singleShot(250, exit_window)
    main_window.close()
    main_window.delete_backup()
