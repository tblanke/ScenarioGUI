import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_push_button_layout_change(qtbot):
    """
    test if the button layout is changed while overing over it

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
    # check if the layout is the small one at the beginning
    for page_i in main_window.gui_structure.list_of_pages:
        assert page_i.button.iconSize() == main_window.size_b
        assert page_i.button.size() == main_window.size_push_s
    # enter and leave all buttons and check if they all have the correct size
    for page in main_window.gui_structure.list_of_pages:
        main_window.eventFilter(page.button, QtC.QEvent(QtC.QEvent.Enter))
        for page_i in main_window.gui_structure.list_of_pages:
            assert page_i.button.size() == main_window.size_push_b
            assert page_i.button.iconSize() == main_window.size_s
        qtbot.wait(50)
        main_window.eventFilter(page.button, QtC.QEvent(QtC.QEvent.Leave))
        for page_i in main_window.gui_structure.list_of_pages:
            assert page_i.button.iconSize() == main_window.size_b
            assert page_i.button.size() == main_window.size_push_s

    main_window.delete_backup()
