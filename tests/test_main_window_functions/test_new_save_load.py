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


def test_save_load_new(qtbot):
    """
    test if load, save and create a new scenario works

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(1.1)
    main_window.gui_structure.int_a.set_value(10)
    main_window.gui_structure.list_small_2.set_value(2)
    main_window.start_current_scenario_calculation(True)
    with qtbot.waitSignal(main_window.threads[0].any_signal, raising=False):
        main_window.threads[0].run()
        main_window.threads[0].any_signal.connect(main_window.thread_function)

    main_window.save_scenario()
    # set filenames
    filename_1 = f"test_1.{global_vars.FILE_EXTENSION}"
    filename_2 = f"test_2.{global_vars.FILE_EXTENSION}"
    filename_3 = f"test_3.{global_vars.FILE_EXTENSION}"
    # delete files if they already exists
    if os.path.exists(main_window.default_path.joinpath(filename_1)):  # pragma: no cover
        os.remove(main_window.default_path.joinpath(filename_1))
    if os.path.exists(main_window.default_path.joinpath(filename_2)):  # pragma: no cover
        os.remove(main_window.default_path.joinpath(filename_2))
    if os.path.exists(main_window.default_path.joinpath(filename_3)):  # pragma: no cover
        os.remove(main_window.default_path.joinpath(filename_3))
    # trigger save action and add filename
    QtC.QTimer.singleShot(100, lambda: keyboard.press("Esc"))
    main_window.action_save.trigger()
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (Path(main_window.filename_default[0]), main_window.filename_default[1])
    # trigger save action and add filename
    QtC.QTimer.singleShot(1000, lambda: keyboard.write(filename_1))
    QtC.QTimer.singleShot(1200, lambda: keyboard.press("enter"))
    main_window.action_save.trigger()
    # check if filename is set correctly
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (
        main_window.default_path.joinpath(filename_1),
        f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})",
    )
    # check if filename is set correctly
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (
        main_window.default_path.joinpath(filename_1),
        f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})",
    )
    # get old list and add a new scenario
    list_old = main_window.list_ds.copy()
    main_window.add_scenario()
    # check that they differ
    assert list_old != main_window.list_ds
    # set a different filename and test save as action
    QtC.QTimer.singleShot(1000, lambda: keyboard.write(filename_2))
    QtC.QTimer.singleShot(1200, lambda: keyboard.press("enter"))
    main_window.action_save_as.trigger()
    # check if filename is set correctly
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (
        main_window.default_path.joinpath(filename_2),
        f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})",
    )
    # trigger open function and set filename 1
    QtC.QTimer.singleShot(1000, lambda: keyboard.write(filename_1))
    QtC.QTimer.singleShot(1200, lambda: keyboard.press("enter"))
    main_window.action_open.trigger()
    # check if filename is imported correctly and the data storages as well
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (
        main_window.default_path.joinpath(filename_1),
        f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})",
    )
    # check if the imported values are the same
    for ds_old, ds_new in zip(list_old, main_window.list_ds, strict=True):
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue

    # set a different filename and test new action
    QtC.QTimer.singleShot(1000, lambda: keyboard.write(filename_3))
    QtC.QTimer.singleShot(1200, lambda: keyboard.press("enter"))
    main_window.action_new.trigger()
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (
        main_window.default_path.joinpath(filename_3),
        f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})",
    )
    assert len(main_window.list_ds) < 1
    main_window.filename = (filename_1, filename_1)
    main_window.fun_load_known_filename()
    assert main_window.status_bar.widget.currentMessage() == main_window.translations.no_file_selected[0]
    main_window.delete_backup()
