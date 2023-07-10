import numpy as np
import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_min_max_setting_within_its_default_limits(qtbot):
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
    float_b = main_window.gui_structure.float_b
    float_b.widget.setMaximum(500)
    float_b.set_value(600)
    assert np.isclose(float_b.get_value(), 600)
    float_b.set_value(float_b.maximal_value + 100)
    assert np.isclose(float_b.get_value(), float_b.maximal_value)
    float_b.widget.setMinimum(50)
    float_b.set_value(10)
    assert np.isclose(float_b.get_value(), 10)
    float_b.set_value(float_b.minimal_value - 100)
    assert np.isclose(float_b.get_value(), float_b.minimal_value)
    main_window.delete_backup()
