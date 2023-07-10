import os
from functools import partial
from json import dump, load
from pathlib import Path

import PySide6.QtWidgets as QtW
import numpy as np

from ScenarioGUI.gui_classes.gui_combine_window import JsonDict

from ..starting_closing_tests import close_tests, start_tests


def test_add_other_file_extensions(qtbot):
    """
    test if the GUI handles wrong load and save inputs correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """

    # init gui window
    main_window = start_tests(qtbot)

    def export_txt(file_path: Path, data: JsonDict) -> None:
        # write data to back up file
        with open(file_path, "w") as file:
            dump(data, file, indent=1)

    def import_txt(file_path: Path) -> JsonDict:
        # write data to back up file
        with open(file_path) as file:
            data = load(file)
        return data

    main_window.add_other_export_function("txt", export_txt)
    main_window.add_other_import_function("txt", import_txt)
    main_window.gui_structure.float_b.set_value(150.23)
    # set filenames
    filename_1 = "test_1_txt.txt"
    # delete files if they already exists
    if os.path.exists(main_window.default_path.joinpath(filename_1)):  # pragma: no cover
        os.remove(main_window.default_path.joinpath(filename_1))

    def get_save_file_name(*args, **kwargs):
        """getSaveFileName proxy"""
        return kwargs["return_value"]

    QtW.QFileDialog.getSaveFileName = partial(get_save_file_name, return_value=(f"{main_window.default_path.joinpath(filename_1)}", "txt (.txt)"))
    main_window.fun_save_as()
    assert filename_1 not in main_window.dia.windowTitle()
    close_tests(main_window, qtbot)
    main_window = start_tests(qtbot)
    main_window.add_other_export_function("txt", export_txt)
    main_window.add_other_import_function("txt", import_txt)
    assert not np.isclose(main_window.gui_structure.float_b.get_value(), 150.23)
    QtW.QFileDialog.getOpenFileName = partial(get_save_file_name, return_value=(f"{main_window.default_path.joinpath(filename_1)}", "txt (.txt)"))
    main_window.fun_load()
    assert filename_1 not in main_window.dia.windowTitle()
    assert np.isclose(main_window.gui_structure.float_b.get_value(), 150.23)

    close_tests(main_window, qtbot)
