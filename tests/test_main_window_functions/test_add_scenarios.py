import os
from functools import partial
from pathlib import Path

import numpy as np
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars

from ..starting_closing_tests import close_tests, start_tests


def test_add_scenarios_2_currents(qtbot):  # noqa: PLR0915
    """
    test if load, save and create a new scenario works

    Parameters # noqa: PLR0915
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.activate_load_as_new_scenarios()
    main_window.add_scenario()
    main_window.gui_structure.aim_add.widget.click()
    main_window.gui_structure.float_b.set_value(1.1)
    main_window.gui_structure.int_a.set_value(10)
    main_window.gui_structure.list_small_2.set_value(2)
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(1.5)
    main_window.gui_structure.int_a.set_value(50)
    main_window.gui_structure.list_small_2.set_value(5)
    main_window.gui_structure.aim_sub.widget.click()
    main_window.save_scenario()
    # set filenames
    filename_1 = f"test_1.{global_vars.FILE_EXTENSION}"
    filename_2 = f"test_2.{global_vars.FILE_EXTENSION}"
    # delete files if they already exists
    if os.path.exists(main_window.default_path.joinpath(filename_1)):  # pragma: no cover
        os.remove(main_window.default_path.joinpath(filename_1))
    if os.path.exists(main_window.default_path.joinpath(filename_2)):  # pragma: no cover
        os.remove(main_window.default_path.joinpath(filename_2))

    # trigger save action and add filename

    def get_save_file_name(*args, **kwargs):
        """getSaveFileName proxy"""
        return kwargs["return_value"]

    QtW.QFileDialog.getSaveFileName = partial(
        get_save_file_name, return_value=(f"{main_window.default_path.joinpath(filename_1)}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )
    main_window.action_save_as.trigger()
    for thread in main_window.saving_threads:
        thread.run()
        assert thread.calculated
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (
        main_window.default_path.joinpath(filename_1),
        f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})",
    )

    QtW.QFileDialog.getSaveFileName = partial(
        get_save_file_name, return_value=(f"{main_window.default_path.joinpath(filename_2)}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )
    main_window.action_save_as.trigger()
    for thread in main_window.saving_threads:
        thread.run()
        assert thread.calculated
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (
        main_window.default_path.joinpath(filename_2),
        f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})",
    )
    # get old list and add a new scenario
    list_old = main_window.list_ds.copy()
    assert len(list_old) == 2
    # trigger open function and set filename 1
    QtW.QFileDialog.getOpenFileName = partial(get_save_file_name, return_value=("", ""))
    main_window.action_open_add.trigger()
    # check if filename is imported correctly and the data storages as well
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (
        main_window.default_path.joinpath(filename_2),
        f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})",
    )
    assert len(main_window.list_ds) == 2
    # trigger open function and set filename 1
    QtW.QFileDialog.getOpenFileName = partial(
        get_save_file_name, return_value=(f"{main_window.default_path.joinpath(filename_1)}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )
    assert main_window.dia.windowTitle()[-1] != "*"
    main_window.action_open_add.trigger()
    # check if filename is imported correctly and the data storages as well
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (
        main_window.default_path.joinpath(filename_2),
        f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})",
    )
    assert main_window.dia.windowTitle()[-1] == "*"
    assert len(main_window.list_ds) == 4
    # check if the imported values are the same
    for ds_old, ds_new in zip(list_old, main_window.list_ds[2:]):
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue

    close_tests(main_window, qtbot)
