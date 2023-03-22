import PySide6.QtWidgets as QtW
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_category(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    # check if graphics are created
    assert isinstance(main_window.gui_structure.category_grid.graphic_left, QtW.QGraphicsView)
    assert isinstance(main_window.gui_structure.category_grid.graphic_right, QtW.QGraphicsView)
    # check set text
    main_window.gui_structure.category_language.set_text("Hello")
    assert main_window.gui_structure.category_language.label.text() == "Hello"
    main_window.gui_structure.category_language.show()
    assert not main_window.gui_structure.category_language.is_hidden()
    main_window.gui_structure.category_language.hide()
    assert main_window.gui_structure.category_language.is_hidden()
    main_window.delete_backup()
