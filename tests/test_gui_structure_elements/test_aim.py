import PySide6.QtWidgets as QtW
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_aim(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)

    if not main_window.gui_structure.aim_plot.widget.isChecked():
        main_window.gui_structure.aim_plot.widget.click()

    assert main_window.gui_structure.aim_plot.widget.isChecked()

    main_window.gui_structure.aim_plot.set_text("Hello")
    assert main_window.gui_structure.aim_plot.widget.text() == "Hello"

