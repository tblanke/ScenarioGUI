from __future__ import annotations

from pathlib import Path
from platform import system

import PySide6.QtGui as QtG
import PySide6.QtWidgets as QtW
from pytest import raises

from ScenarioGUI import global_settings as globs
from ScenarioGUI import load_config

from ..starting_closing_tests import close_tests, start_tests


def test_global_settings(qtbot):  # noqa: PLR0915
    """
    test if two scenarios can have the same name.

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    load_config(Path(".").absolute().joinpath("./tests/gui_config.ini") if Path(".").absolute().joinpath("./tests/gui_config.ini").exists() else Path(
        "..").absolute().joinpath("./tests/gui_config.ini"))
    main_window = start_tests(qtbot)
    assert main_window.dia.font().family() == globs.FONT == ("Arial" if system() == "Windows" else 'Helvetica')
    assert main_window.dia.font().pointSize() == (10 if system() == "Windows" else 14) == globs.FONT_SIZE

    assert globs.WHITE == "rgb(255, 255, 255)"
    assert globs.LIGHT == "rgb(84, 188, 235)"
    assert globs.LIGHT_SELECT == "rgb(42, 126, 179)"
    assert globs.DARK == "rgb(0, 64, 122)"
    assert globs.GREY == "rgb(100, 100, 100)"
    assert globs.WARNING == "rgb(255, 200, 87)"
    assert globs.BLACK == "rgb(0, 0, 0)"

    assert globs.FILE_EXTENSION == "scenario"
    assert main_window._backup_filename == "backup.scenarioBackUp"
    assert globs.GUI_NAME == "Scenario GUI"
    assert globs.ICON_NAME == "icon.svg"
    assert globs.path.joinpath(".").parent if "tests" in f"{Path('.').absolute()}" else globs.path.joinpath(".") == globs.FOLDER
    # test get_path_for_file function
    assert globs.get_path_for_file(globs.path.joinpath("./ScenarioGUI/gui_classes/gui_structure_classes"), "gui_config.ini") in [globs.path.parent.joinpath(
        "." if "tests" in f"{Path('.').absolute()}" else "./examples"), globs.path.parent.joinpath("." if "tests" in f"{Path('.').absolute()}" else "./tests")]
    # test combine window settings
    check_font(main_window.push_button_cancel, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.push_button_start_single, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.push_button_start_multiple, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.push_button_add_scenario, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.push_button_delete_scenario, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.push_button_save_scenario, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.button_rename_scenario, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.status_bar.label, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.menu_settings, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.menubar, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.menu_scenario, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.menu_calculation, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.menu_language, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.menu_file, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.progress_bar, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.label_status, globs.FONT_SIZE, globs.FONT, False)
    # test page settings
    check_font(main_window.gui_structure.page_result.label, globs.FONT_SIZE + 4, globs.FONT, True)
    check_font(main_window.gui_structure.page_result.button, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.gui_structure.page_result.push_button_previous, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.gui_structure.page_result.push_button_next, globs.FONT_SIZE, globs.FONT, True)
    # test option settings
    check_font(main_window.gui_structure.int_a.label, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.gui_structure.int_a.widget, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.gui_structure.float_b.label, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.gui_structure.float_b.widget, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.gui_structure.filename.label, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.gui_structure.filename.widget, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.gui_structure.list_box.label, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.gui_structure.list_box.widget, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.gui_structure.function_button.button, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.gui_structure.button_box.label, globs.FONT_SIZE, globs.FONT, False)
    [check_font(widget, globs.FONT_SIZE, globs.FONT, True) for widget in main_window.gui_structure.button_box.widget]
    check_font(main_window.gui_structure.hint_flex.label, globs.FONT_SIZE, globs.FONT, False)
    check_font(main_window.gui_structure.aim_add.widget, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.gui_structure.category_inputs.label, globs.FONT_SIZE, globs.FONT, True)
    check_font(main_window.gui_structure.flex_option.label, globs.FONT_SIZE, globs.FONT, True)
    [check_font(widget, globs.FONT_SIZE, globs.FONT, isinstance(widget, QtW.QPushButton)) for widget in main_window.gui_structure.flex_option.frame.children()
     if
     isinstance(widget, QtW.QWidget)]

    # test file not found error
    with raises(FileNotFoundError):
        assert globs.path == globs.get_path_for_file(globs.path.joinpath("./ScenarioGUI/gui_classes/gui_structure_classes"), "not_exists.ini")

    close_tests(main_window, qtbot)


def check_font(widget: QtW.QWidget | QtG.QAction, size: int, font_name: str, bold: bool):
    font = widget.font()
    assert font.family() == font_name
    assert font.pointSize() == size
    assert font.bold() == bold
