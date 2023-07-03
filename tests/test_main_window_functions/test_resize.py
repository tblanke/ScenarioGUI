import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_resize_event_button_sizes(qtbot):
    """
    test if the resize event is changing the button size

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.dia.setFixedSize(QtC.QSize(150,150))
    main_window.resizeEvent(None)
    assert main_window.size_push_s.height() < 75
    assert main_window.size_push_b.height() < 75
    main_window.dia.setFixedSize(QtC.QSize(1500,1500))
    main_window.resizeEvent(None)
    assert main_window.size_push_s.height() == 75
    assert main_window.size_push_b.height() == 75