import os
from functools import partial
from json import dump, load

import numpy as np
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import JsonDict

from ..starting_closing_tests import close_tests, start_tests


def test_add_other_version_functions(qtbot):
    """
    test if the GUI handles wrong load and save inputs correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """

    # init gui window
    main_window = start_tests(qtbot)

    def other_version_import(data: JsonDict) -> JsonDict:
        for dic in data["values"]:
            dic["float_b"] = dic["float_b"] + 10
        return data

    main_window.add_other_version_import_function("v0.0.1", other_version_import)
    # set filenames
    filename_1 = f"test_1.{global_vars.FILE_EXTENSION}"
    # delete files if they already exists
    if os.path.exists(main_window.default_path.joinpath(filename_1)):  # pragma: no cover
        os.remove(main_window.default_path.joinpath(filename_1))

    def get_save_file_name(*args, **kwargs):
        """getSaveFileName proxy"""
        return kwargs["return_value"]

    QtW.QFileDialog.getSaveFileName = partial(
        get_save_file_name, return_value=(f"{main_window.default_path.joinpath(filename_1)}", f"{global_vars.FILE_EXTENSION} (.{global_vars.FILE_EXTENSION})")
    )
    main_window.fun_save_as()
    for thread in main_window.saving_threads:
        thread.run()
        assert thread.calculated
    assert filename_1 in main_window.dia.windowTitle()
    old_value = main_window.gui_structure.float_b.get_value()
    qtbot.wait(1000)

    with open(main_window.default_path.joinpath(filename_1)) as file:
        saving = load(file)

    saving["version"] = "0.0.1"

    with open(main_window.default_path.joinpath(filename_1), "w") as file:
        dump(saving, file, indent=1)

    close_tests(main_window, qtbot)
    main_window = start_tests(qtbot)
    main_window.add_other_version_import_function("v0.0.1", other_version_import)

    assert not np.isclose(main_window.gui_structure.float_b.get_value(), old_value + 10)
    QtW.QFileDialog.getOpenFileName = partial(get_save_file_name, return_value=(f"{main_window.default_path.joinpath(filename_1)}",
                                                                                f"{global_vars.FILE_EXTENSION} (.{global_vars.FILE_EXTENSION})"))
    main_window.fun_load()
    assert filename_1 in main_window.dia.windowTitle()
    assert np.isclose(main_window.gui_structure.float_b.get_value(), old_value + 10)
    close_tests(main_window, qtbot)
