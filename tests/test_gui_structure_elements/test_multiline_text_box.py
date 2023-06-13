import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_multiline_text_box(qtbot):
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

    main_window.gui_structure.text_box_multi_line._init_links()

    assert main_window.gui_structure.text_box_multi_line.get_value() == main_window.gui_structure.text_box_multi_line.default_value
    main_window.gui_structure.text_box_multi_line.set_value("Hello\nWorld")
    assert main_window.gui_structure.text_box_multi_line.get_value() == "Hello\nWorld"

    assert main_window.gui_structure.text_box_multi_line.check_linked_value("Hello\nWorld")

    # test set text
    main_window.gui_structure.text_box_multi_line.set_text("Hello")
    assert main_window.gui_structure.text_box_multi_line.label.text() == "Hello"
    main_window.delete_backup()



