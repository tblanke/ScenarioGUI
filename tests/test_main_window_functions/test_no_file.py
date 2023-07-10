import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..starting_closing_tests import close_tests, start_tests
from ..test_translations.translation_class import Translations


def test_no_load_save_file(qtbot):
    """
    test if the GUI handles wrong load and save inputs correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """

    # init gui window
    main_window = start_tests(qtbot)
    # check if an import error has been raises with a wrong load file
    main_window._load_from_data(f"not_there.{global_vars.FILE_EXTENSION}")
    assert main_window.status_bar.label.text() == main_window.translations.no_file_selected[0]
    # check if the current error message is shown with a wrong save file/folder
    main_window._save_to_data(f"hello/not_there.{global_vars.FILE_EXTENSION}")
    assert main_window.status_bar.label.text() == main_window.translations.no_file_selected[main_window.gui_structure.option_language.get_value()[0]]
    close_tests(main_window, qtbot)
