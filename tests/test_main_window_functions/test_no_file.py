import PySide6.QtWidgets as QtW
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results


def test_no_load_save_file(qtbot):
    """
    test if the GUI handles wrong load and save inputs correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """

    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    # check if an import error has been raises with a wrong load file
    main_window._load_from_data("not_there.GHEtool")
    assert main_window.status_bar.widget.currentMessage() == main_window.translations.no_file_selected[0]
    # check if the current error message is shown with a wrong save file/folder
    main_window._save_to_data("hello/not_there.GHEtool")
    assert main_window.status_bar.widget.currentMessage() == main_window.translations.no_file_selected[main_window.gui_structure.option_language.get_value()[0]]
    main_window.delete_backup()
