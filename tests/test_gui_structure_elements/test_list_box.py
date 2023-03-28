import PySide6.QtWidgets as QtW
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from tests.gui_structure_for_tests import GUI
from tests.result_creating_class_for_tests import ResultsClass, data_2_results
from tests.test_translations.translation_class import Translations


def test_list_box(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    # test set value
    assert main_window.gui_structure.list_small_2.get_value()[0] == main_window.gui_structure.list_small_2.default_value
    main_window.gui_structure.list_small_2.set_value(main_window.gui_structure.list_small_2.default_value + 1)
    assert main_window.gui_structure.list_small_2.get_value()[0] == main_window.gui_structure.list_small_2.default_value + 1
    # test links
    main_window.gui_structure.list_small_2.set_value(0)
    assert main_window.gui_structure.hint_2.is_hidden()
    main_window.gui_structure.list_small_2.set_value(1)
    assert not main_window.gui_structure.hint_2.is_hidden()
    # test set text
    main_window.gui_structure.list_box.set_text("Hello,4,5,6,7")
    assert main_window.gui_structure.list_box.label.text() == "Hello"
    for i, val in zip(range(4), ["4", "5", "6", "7"]):
        assert main_window.gui_structure.list_box.widget.itemText(i) == val

    main_window.gui_structure.list_small_2.set_value(2)
    assert main_window.gui_structure.list_small_2.get_value()[0] == 2
    main_window.gui_structure.list_small_2.set_value((3, "Hi"))
    assert main_window.gui_structure.list_small_2.get_value() == (3, "3")
    main_window.gui_structure.list_small_2._init_links()
    assert main_window.gui_structure.list_small_2.get_value() == (3, "3")

    main_window.delete_backup()
