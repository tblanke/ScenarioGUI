import os
from pathlib import Path

import keyboard
import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW
import numpy as np

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_backup(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(1.1)
    main_window.gui_structure.int_a.set_value(10)
    main_window.save_scenario()
    list_old = main_window.list_ds.copy()

    main_window.load_backup()
    # check if the imported values are the same
    for ds_old, ds_new in zip(list_old, main_window.list_ds, strict=True):
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue

    main_window.start_current_scenario_calculation(True)
    with qtbot.waitSignal(main_window.threads[0].any_signal, raising=False):
        main_window.threads[0].run()
        main_window.threads[0].any_signal.connect(main_window.thread_function)

    main_window.save_scenario()
    list_old = main_window.list_ds.copy()
    main_window.load_backup()
    # check if the imported values are the same
    for ds_old, ds_new in zip(list_old, main_window.list_ds, strict=True):
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue

    main_window.delete_backup()
