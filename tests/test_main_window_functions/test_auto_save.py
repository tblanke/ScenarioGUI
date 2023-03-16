from math import isclose

import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations

from ..gui_structure_for_tests import GUI

from ..result_creating_class_for_tests import ResultsClass, data_2_results
global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_auto_save(qtbot):
    """
    test if the auto save function works

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    # set auto save function and create new backup file
    main_window.gui_structure.option_auto_saving.set_value(1)
    main_window.fun_save_auto()
    # add a new scenario and change conductivity
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(2.1)
    # add a new scenario and change conductivity
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(1.1)
    # run calculations
    main_window.action_start_multiple.trigger()
    # check if options has been stored correctly
    assert isclose(main_window.list_ds[1].float_b, 2.1)
    assert isclose(main_window.list_ds[2].float_b, 1.1)
    for _ in main_window.list_ds:
        main_window.delete_scenario()
        qtbot.wait(100)
    assert len(main_window.list_ds) == 1
    assert main_window.list_widget_scenario.count() == 1
    # check if adding a scenario is adding one
    for i in range(10):
        main_window.add_scenario()
        assert len(main_window.list_ds) == 2 + i
        assert main_window.list_widget_scenario.count() == 2 + i
    # check if deleting a scenario is removing a scenario
    for i in range(10):
        main_window.delete_scenario()
        assert len(main_window.list_ds) == 10 - i
        assert main_window.list_widget_scenario.count() == 10 - i
    # check if deleting the last scenario is ignored so at least one exists
    main_window.delete_scenario()
    assert len(main_window.list_ds) == 1
    assert main_window.list_widget_scenario.count() == 1
    main_window.delete_backup()
    