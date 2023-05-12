import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from tests.gui_structure_for_tests import GUI
from tests.result_creating_class_for_tests import ResultsClass, data_2_results
from tests.test_translations.translation_class import Translations


def test_page(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)

    main_window.gui_structure.page_result.set_text("button name,Name")
    assert main_window.gui_structure.page_result.button.text() == "button name"
    assert main_window.gui_structure.page_result.label.text() == "Name"

    # test linked function which counts the counter every time button is clicked
    assert main_window.gui_structure.counter == 1
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.counter == 2
    # check that 3 aim are in a row
    scroll_area = [widget for widget in main_window.gui_structure.page_inputs.page.children() if isinstance(widget, QtW.QScrollArea)][0]
    assert scroll_area.children()[0].children()[0].children()[1].children()[0].rowCount() == 1
    assert scroll_area.children()[0].children()[0].children()[1].children()[0].columnCount() == 4
    main_window.delete_backup()
