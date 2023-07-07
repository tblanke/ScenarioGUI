import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_result_text_on_on_result_page(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    # check if graphics are created
    gs = main_window.gui_structure

    assert not gs.result_text_not_on_result_page.is_hidden()

    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    qtbot.wait(1500)
    assert gs.result_text_add.label.text() == "Result: m"
