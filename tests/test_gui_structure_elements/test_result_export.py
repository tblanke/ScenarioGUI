import os
from functools import partial
from pathlib import Path

import PySide6.QtWidgets as QtW

from tests.starting_closing_tests import close_tests, start_tests


def test_results_export(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    folder = Path(__file__).parent.parent
    file = f'{folder.joinpath("./test_export.txt")}'
    # delete files if they already exists
    if os.path.exists(main_window.default_path.joinpath(file)):  # pragma: no cover
        os.remove(main_window.default_path.joinpath(file))

    def get_save_file_name(*args, **kwargs):
        """getSaveFileName proxy"""
        return kwargs["return_value"]

    QtW.QFileDialog.getSaveFileName = partial(get_save_file_name, return_value=(f"{file}", f"{main_window.filename_default[1]}"))
    main_window.gui_structure.export_results.button.click()
    with open(file) as f:
        data = f.read()

    assert data == f"result: {main_window.list_ds[main_window.list_widget_scenario.currentRow()].results.result}"

    # test set text
    main_window.gui_structure.export_results.set_text("Hello,Set")
    assert main_window.gui_structure.export_results.button.text() == "Hello"
    assert main_window.gui_structure.export_results.caption == "Set"

    os.remove(main_window.default_path.joinpath(file))
    close_tests(main_window, qtbot)
