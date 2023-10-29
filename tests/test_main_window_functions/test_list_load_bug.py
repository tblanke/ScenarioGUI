from ..starting_closing_tests import close_tests, start_tests
import ScenarioGUI.global_settings as global_vars


import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations

def test_list_load_bug(qtbot):
    """
    test if the deleting of scenario is performed correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    filename = main_window.default_path.joinpath(f"test_2.{global_vars.FILE_EXTENSION}")
    main_window.gui_structure.list_box.set_value(2)
    main_window.save_scenario()
    main_window._save_to_data(f"{filename}")
    main_window._save_to_data(main_window.backup_file)
    main_window.gui_structure.list_box.set_value(0)
    assert main_window.gui_structure.list_box.get_value()[0] == 0
    main_window.load_backup()
    assert main_window.gui_structure.list_box.get_value()[0] == 2
    main_window.add_scenario()
    assert main_window.gui_structure.list_box.get_value()[0] == 2
    main_window._save_to_data(f"{filename}")
    main_window._save_to_data(main_window.backup_file)
    main_window.gui_structure.list_box.set_value(0)
    assert main_window.gui_structure.list_box.get_value()[0] == 0
    main_window.load_backup()
    assert main_window.gui_structure.list_box.get_value()[0] == 2
    close_tests(main_window, qtbot)
