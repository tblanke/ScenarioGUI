import PySide6.QtWidgets as QtW
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results


def test_language(qtbot):
    """
    test if the language is changed correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()

    for idx, action in enumerate(main_window.menu_language.actions()):
        action.trigger()
        assert main_window.gui_structure.option_language.get_value()[0] == idx

    main_window.menu_language.actions()[0].trigger()
    main_window.delete_backup()
