import os
from functools import partial
from pathlib import Path

import PySide6.QtWidgets as QtW
from sys import setrecursionlimit

from ..starting_closing_tests import close_tests, start_tests
setrecursionlimit(1500)

import ScenarioGUI.global_settings as global_vars


def test_saving_a_moved_fie(qtbot):

    def get_save_file_name(*args, **kwargs):
        """getSaveFileName proxy"""
        return kwargs["return_value"]

    main_window = start_tests(qtbot)
    filename1 = main_window.default_path.joinpath(f"test/temp.{global_vars.FILE_EXTENSION}")
    filename2 = main_window.default_path.joinpath(f"tests/temp2.{global_vars.FILE_EXTENSION}")
    filename1.parent.mkdir(parents=True, exist_ok=True)
    filename2.parent.mkdir(parents=True, exist_ok=True)
    # trigger save action and add filename
    QtW.QFileDialog.getSaveFileName = partial(
        get_save_file_name, return_value=(f"{filename1}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )
    QtW.QFileDialog.getOpenFileName = partial(
        get_save_file_name, return_value=(f"{filename2}", f"{global_vars.FILE_EXTENSION} (*.{global_vars.FILE_EXTENSION})")
    )
    main_window.action_save_as.trigger()
    assert Path(main_window.filename[0]) == filename1
    thread = main_window.saving_threads[-1]
    thread.run()
    assert thread.calculated
    os.replace(filename1, filename2)
    main_window.action_open.trigger()
    main_window.fun_save()
    assert Path(main_window.filename[0]) == filename2
    close_tests(main_window, qtbot)
    assert not os.path.exists(filename1)
    assert os.path.exists(filename2)
    filename1.parent.rmdir()
    filename2.unlink()
    filename2.parent.rmdir()
