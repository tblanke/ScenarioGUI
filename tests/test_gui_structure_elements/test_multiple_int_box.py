import numpy as np
import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_multiple_int_box(qtbot):
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
    multiple_ints = main_window.gui_structure.multiple_ints
    assert np.allclose(multiple_ints.get_value(), multiple_ints.default_value)
    multiple_ints.set_value((multiple_ints.default_value[0] + 5, multiple_ints.default_value[1] + 5, multiple_ints.default_value[2] + 5))
    assert np.allclose((multiple_ints.default_value[0] + 5, multiple_ints.default_value[1] + 5, multiple_ints.default_value[2] + 5), multiple_ints.get_value())
    multiple_ints._init_links()
    assert multiple_ints.check_linked_value((20, None))
    assert multiple_ints.check_linked_value((None, 2))
    assert not multiple_ints.check_linked_value((5, 20))
    multiple_ints.show_option(main_window.gui_structure.float_b, 5, 20)
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.float_b.is_hidden()
    multiple_ints.set_value((4, 6, 7))
    multiple_ints.show_option(main_window.gui_structure.float_b, 5, 20)
    assert not main_window.gui_structure.float_b.is_hidden()
    multiple_ints.set_value((6,7,22))
    multiple_ints.show_option(main_window.gui_structure.float_b, 5, 20)
    assert not main_window.gui_structure.float_b.is_hidden()
    multiple_ints.add_link_2_show(main_window.gui_structure.float_b, below=5, above=20)
    multiple_ints.set_value((10, 11 ,12))
    assert main_window.gui_structure.float_b.is_hidden()
    multiple_ints.set_value((4,6,7))
    assert not main_window.gui_structure.float_b.is_hidden()
    multiple_ints.set_value((6,22,7))
    assert not main_window.gui_structure.float_b.is_hidden()
    main_window.delete_backup()
