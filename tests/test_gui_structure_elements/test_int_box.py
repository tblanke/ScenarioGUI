import numpy as np
import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_int_box(qtbot):
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
    int_a = main_window.gui_structure.int_a
    assert np.isclose(int_a.get_value(), int_a.default_value)
    int_a.set_value(int_a.default_value + 5)
    assert np.isclose(int_a.default_value + 5, int_a.get_value())
    int_a._init_links()
    assert int_a.check_linked_value((20, None))
    assert int_a.check_linked_value((None, 2))
    assert not int_a.check_linked_value((5, 20))
    int_a.show_option(main_window.gui_structure.float_b, 5, 20)
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.float_b.is_hidden()
    int_a.set_value(4)
    int_a.show_option(main_window.gui_structure.float_b, 5, 20)
    assert not main_window.gui_structure.float_b.is_hidden()
    int_a.set_value(22)
    int_a.show_option(main_window.gui_structure.float_b, 5, 20)
    assert not main_window.gui_structure.float_b.is_hidden()
    int_a.add_link_2_show(main_window.gui_structure.float_b, below=5, above=20)
    int_a.set_value(10)
    assert main_window.gui_structure.float_b.is_hidden()
    int_a.set_value(4)
    assert not main_window.gui_structure.float_b.is_hidden()
    int_a.set_value(22)
    assert not main_window.gui_structure.float_b.is_hidden()
    main_window.delete_backup()
