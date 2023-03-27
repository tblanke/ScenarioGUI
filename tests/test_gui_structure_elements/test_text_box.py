import PySide6.QtWidgets as QtW
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results


def test_text_box(qtbot):
    """
    test text box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)

    main_window.gui_structure.text_box._init_links()

    assert main_window.gui_structure.text_box.get_value() == main_window.gui_structure.text_box.default_value
    main_window.gui_structure.text_box.set_value("Hello")
    assert main_window.gui_structure.text_box.get_value() == "Hello"

    assert main_window.gui_structure.text_box.check_linked_value("Hello")

    # test set text
    main_window.gui_structure.text_box.set_text("Hello")
    assert main_window.gui_structure.text_box.label.text() == "Hello"
    main_window.delete_backup()



