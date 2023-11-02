import os
from functools import partial

import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as globs

from ..starting_closing_tests import close_tests, start_tests


def test_close(qtbot):
    """
    test if the close dialog works correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """

    # init gui window
    main_window = start_tests(qtbot)
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(2.1)
    # set filenames
    filename_1 = f"test_1.{globs.FILE_EXTENSION}"
    # delete files if they already exists
    if os.path.exists(main_window.default_path.joinpath(filename_1)):  # pragma: no cover
        os.remove(main_window.default_path.joinpath(filename_1))

    response = QtW.QMessageBox.Cancel

    class NewMessageBox(QtW.QMessageBox):
        def exec(self):
            return response

    QtW.QMessageBox = NewMessageBox
    main_window.close()

    def get_save_file_name(*args, **kwargs):
        """getSaveFileName proxy"""
        return kwargs["return_value"]

    QtW.QFileDialog.getSaveFileName = partial(get_save_file_name, return_value=("", ""))
    response = QtW.QMessageBox.Save
    main_window.close()

    assert len(main_window.saving_threads) == 0

    QtW.QFileDialog.getSaveFileName = partial(get_save_file_name, return_value=(f"{main_window.default_path.joinpath(filename_1)}", f"{main_window.filename_default[1]}"))
    response = QtW.QMessageBox.Save
    main_window.close()
    assert filename_1 in main_window.filename[0]
    assert filename_1 in main_window.dia.windowTitle()
    for thread in main_window.saving_threads:
        assert thread.isFinished()
        assert thread.calculated

    response = QtW.QMessageBox.Close
    main_window.close()
    close_tests(main_window, qtbot)
