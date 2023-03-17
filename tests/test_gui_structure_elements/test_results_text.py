import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from tests.gui_structure_for_tests import GUI
from tests.result_creating_class_for_tests import ResultsClass, data_2_results
from tests.test_translations.translation_class import Translations

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_results_text(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    # get sum
    sum_ab = main_window.gui_structure.int_a.get_value() + main_window.gui_structure.float_b.get_value()
    main_window.gui_structure.result_text_add.set_text("Hello,kW")
    # calc sum from gui
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    with qtbot.waitSignal(main_window.threads[0].any_signal, raising=False):
        QtW.QApplication.processEvents()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    # check text output
    assert main_window.gui_structure.result_text_add.label.text() == f"Hello{sum_ab}kW"
    main_window.delete_backup()
