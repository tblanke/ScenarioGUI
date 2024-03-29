import os
from functools import partial
from pathlib import Path

import numpy as np
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars

from ..starting_closing_tests import close_tests, start_tests


def test_save_load_new(qtbot):  # noqa: PLR0915
    """
    test if load, save and create a new scenario works

    Parameters # noqa: PLR0915
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.gui_structure.float_b.set_value(1.1)
    main_window.gui_structure.int_a.set_value(10)
    main_window.gui_structure.list_small_2.set_value(2)
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    main_window.save_scenario()
    # set filenames
    filename_1 = main_window.default_path.joinpath(f"/test/test_1.{global_vars.FILE_EXTENSION}")
    filename_2 = main_window.default_path.joinpath(f"test_2.{global_vars.FILE_EXTENSION}")
    filename_3 = main_window.default_path.joinpath(f"test_3.{global_vars.FILE_EXTENSION}")
    # delete files if they already exists
    if os.path.exists(filename_1):  # pragma: no cover
        os.remove(filename_1)
    if os.path.exists(filename_2):  # pragma: no cover
        os.remove(filename_2)
    if os.path.exists(filename_3):  # pragma: no cover
        os.remove(filename_3)

    # trigger save action and add filename

    def get_save_file_name(*args, **kwargs):
        """getSaveFileName proxy"""
        return kwargs["return_value"]

    QtW.QFileDialog.getSaveFileName = partial(get_save_file_name, return_value=(f"{main_window.filename_default[0]}", f"{main_window.filename_default[1]}"))
    main_window.action_save.trigger()
    thread = main_window.saving_threads[0]
    thread.run()
    assert thread.calculated
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (Path(main_window.filename_default[0]), main_window.filename_default[1])
    # trigger save action and add filename
    QtW.QFileDialog.getSaveFileName = partial(
        get_save_file_name, return_value=(f"{filename_1}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )
    main_window.action_save.trigger()
    thread = main_window.saving_threads[0]
    thread.run()
    assert thread.calculated
    # check if filename is set correctly
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (filename_1, f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    assert f"{filename_1.parent}" == f"{main_window.default_path}"
    main_window.action_save.trigger()
    thread = main_window.saving_threads[0]
    thread.run()
    assert thread.calculated
    # check if filename is set correctly
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (filename_1, f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    # get old list and add a new scenario
    list_old = main_window.list_ds.copy()
    main_window.add_scenario()
    # check that they differ
    assert list_old != main_window.list_ds
    # set a different filename and test save as action
    QtW.QFileDialog.getSaveFileName = partial(
        get_save_file_name, return_value=(f"{filename_2}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )
    main_window.action_save_as.trigger()
    thread = main_window.saving_threads[0]
    thread.run()
    assert thread.calculated
    # check if filename is set correctly
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (filename_2, f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    assert f"{filename_2.parent}" == f"{main_window.default_path}"
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    main_window.fun_save(main_window.filename)
    main_window._save_to_data(main_window.filename[0])
    # trigger open function and set filename 1
    QtW.QFileDialog.getOpenFileName = partial(
        get_save_file_name, return_value=(f"{filename_1}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )
    main_window.gui_structure.float_b.set_value(main_window.gui_structure.float_b.get_value() + 1)
    response = QtW.QMessageBox.Cancel

    class NewMessageBox(QtW.QMessageBox):
        def exec(self):
            return response

    QtW.QMessageBox = NewMessageBox
    main_window.action_open.trigger()
    # check if filename is imported correctly and the data storages as well
    assert (Path(main_window.filename[0]), main_window.filename[1]) != (filename_1, f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    assert f"{filename_1.parent}" != f"{main_window.default_path}"
    assert main_window.dia.windowTitle()[-1] == "*"
    response = QtW.QMessageBox.Save
    main_window.action_open.trigger()
    # check if filename is imported correctly and the data storages as well
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (filename_1, f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    assert f"{filename_1.parent}" == f"{main_window.default_path}"
    assert main_window.dia.windowTitle()[-1] != "*"
    # check if the imported values are the same
    for ds_old, ds_new in zip(list_old, main_window.list_ds):
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue
    QtW.QFileDialog.getOpenFileName = partial(
        get_save_file_name, return_value=(f"{filename_2}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )
    response = QtW.QMessageBox.Close
    main_window.gui_structure.float_b.set_value(main_window.gui_structure.float_b.get_value() + 1)
    main_window.action_open.trigger()
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (filename_2, f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    assert f"{filename_2.parent}" == f"{main_window.default_path}"
    assert main_window.dia.windowTitle()[-1] != "*"

    main_window._load_from_data(main_window.filename[0])
    # set a different filename and test new action
    QtW.QFileDialog.getSaveFileName = partial(
        get_save_file_name, return_value=(f"{filename_3}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )

    # trigger open function and set filename 1
    QtW.QFileDialog.getOpenFileName = partial(get_save_file_name, return_value=("", ""))
    main_window.action_open.trigger()
    for ds_old, ds_new in zip(list_old, main_window.list_ds):
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue
    # set a different filename and test new action
    QtW.QFileDialog.getSaveFileName = partial(
        get_save_file_name, return_value=(f"{filename_3}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )
    main_window.gui_structure.float_b.set_value(main_window.gui_structure.float_b.get_value() + 1)
    response = QtW.QMessageBox.Cancel
    main_window.action_new.trigger()
    assert (Path(main_window.filename[0]), main_window.filename[1]) != (filename_3, f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    assert len(main_window.list_ds) != 1
    response = QtW.QMessageBox.Save
    main_window.action_new.trigger()
    assert (Path(main_window.filename[0]), main_window.filename[1]) == (filename_3, f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    assert len(main_window.list_ds) == 1
    main_window.filename = (f"filename_1.{global_vars.FILE_EXTENSION}", filename_1)
    main_window.fun_load_known_filename()
    assert main_window.status_bar.label.text() == main_window.translations.no_file_selected[0]
    close_tests(main_window, qtbot)
