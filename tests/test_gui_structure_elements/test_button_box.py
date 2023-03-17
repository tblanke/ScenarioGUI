import numpy as np
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ..test_translations.translation_class import Translations

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_button_box(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    button_box = main_window.gui_structure.button_box
    assert np.isclose(button_box.get_value(), button_box.default_value)
    button_box.set_value(button_box.default_value + 1)
    assert np.isclose(button_box.default_value + 1, button_box.get_value())
    button_box._init_links()
    assert button_box.check_linked_value(button_box.default_value + 1)
    assert not button_box.check_linked_value(button_box.default_value)
    button_box.add_link_2_show(main_window.gui_structure.int_a, on_index=0)
    button_box.set_value(button_box.default_value)
    button_box.set_value(button_box.default_value + 1)
    assert main_window.gui_structure.int_a.is_hidden()
    button_box.set_value(button_box.default_value)
    assert not main_window.gui_structure.int_a.is_hidden()
    main_window.delete_backup()
