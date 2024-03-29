from functools import partial
from pathlib import Path

import PySide6.QtWidgets as QtW
import pytest

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning

from ..starting_closing_tests import close_tests, start_tests


def test_filename_read(qtbot) -> None:
    """
    test filename reading function

    Parameters
    ----------
    qtbot: qtbot
        qtbot
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()

    folder = Path(__file__).parent.parent
    file = f'{folder.joinpath("./example_data.csv")}'
    assert main_window.gui_structure.filename.get_value() == main_window.gui_structure.filename.default_value
    assert main_window.gui_structure.filename.default_value == file

    # check if no file is passed
    def get_save_file_name(*args, **kwargs):
        """getSaveFileName proxy"""
        return kwargs["return_value"]

    QtW.QFileDialog.getOpenFileName = partial(get_save_file_name, return_value=("", ""))
    main_window.gui_structure.filename.button.click()
    assert main_window.status_bar.label.text() == main_window.gui_structure.filename.error_text
    # check file import and calculation

    QtW.QFileDialog.getOpenFileName = partial(get_save_file_name, return_value=(f"{main_window.default_path.joinpath(file)}", "csv (*.csv"))
    main_window.gui_structure.filename.button.click()
    assert main_window.gui_structure.filename.get_value() == file
    assert main_window.gui_structure.filename.check_linked_value(file)
    assert main_window.gui_structure.filename.create_function_2_check_linked_value(file)() == main_window.gui_structure.filename.check_linked_value(file)
    main_window.save_scenario()
    assert "filename" in main_window.list_ds[0].to_dict()

    main_window.gui_structure.filename.add_link_2_show(main_window.gui_structure.hint_1, "1")
    assert not main_window.gui_structure.hint_1.is_hidden()
    main_window.gui_structure.filename.set_value("1")
    assert not main_window.gui_structure.hint_1.is_hidden()

    with pytest.warns(ConditionalVisibilityWarning):
        main_window.gui_structure.filename.add_link_2_show(main_window.gui_structure.hint_1, "0")

    close_tests(main_window, qtbot)
