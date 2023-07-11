from __future__ import annotations

import PySide6.QtGui as QtG
import PySide6.QtWidgets as QtW

from ..starting_closing_tests import close_tests, start_tests


def test_change_font_size(qtbot):
    """
    test if two scenarios can have the same name.

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.gui_structure.option_font_size.set_value(8)

    check_font_size(main_window.push_button_cancel, 8)
    check_font_size(main_window.push_button_start_single, 8)
    check_font_size(main_window.push_button_start_multiple, 8)
    check_font_size(main_window.push_button_add_scenario, 8)
    check_font_size(main_window.push_button_delete_scenario, 8)
    check_font_size(main_window.push_button_save_scenario, 8)
    check_font_size(main_window.button_rename_scenario, 8)
    check_font_size(main_window.status_bar.label, 8)
    check_font_size(main_window.menu_settings, 8)
    check_font_size(main_window.menubar, 8)
    check_font_size(main_window.menu_scenario, 8)
    check_font_size(main_window.menu_calculation, 8)
    check_font_size(main_window.menu_language, 8)
    check_font_size(main_window.menu_file, 8)
    check_font_size(main_window.progress_bar, 8)
    check_font_size(main_window.label_status, 8)
    # test page settings
    check_font_size(main_window.gui_structure.page_result.label, 8 + 4)
    check_font_size(main_window.gui_structure.page_result.button, 8)
    check_font_size(main_window.gui_structure.page_result.push_button_previous, 8)
    check_font_size(main_window.gui_structure.page_result.push_button_next, 8)
    # test option settings
    check_font_size(main_window.gui_structure.int_a.label, 8)
    check_font_size(main_window.gui_structure.int_a.widget, 8)
    check_font_size(main_window.gui_structure.float_b.label, 8)
    check_font_size(main_window.gui_structure.float_b.widget, 8)
    check_font_size(main_window.gui_structure.filename.label, 8)
    check_font_size(main_window.gui_structure.filename.widget, 8)
    check_font_size(main_window.gui_structure.list_box.label, 8)
    check_font_size(main_window.gui_structure.list_box.widget, 8)
    check_font_size(main_window.gui_structure.float_units.label, 8)
    check_font_size(main_window.gui_structure.float_units.widget, 8)
    check_font_size(main_window.gui_structure.float_units.unit_widget, 8)
    check_font_size(main_window.gui_structure.int_units.label, 8)
    check_font_size(main_window.gui_structure.int_units.widget, 8)
    check_font_size(main_window.gui_structure.int_units.unit_widget, 8)
    check_font_size(main_window.gui_structure.function_button.button, 8)
    check_font_size(main_window.gui_structure.button_box.label, 8)
    [check_font_size(widget, 8) for widget in main_window.gui_structure.button_box.widget]
    check_font_size(main_window.gui_structure.hint_flex.label, 8)
    check_font_size(main_window.gui_structure.aim_add.widget, 8)
    check_font_size(main_window.gui_structure.category_inputs.label, 8)
    check_font_size(main_window.gui_structure.flex_option.label, 8)
    [check_font_size(widget, 8) for widget in main_window.gui_structure.flex_option.frame.children() if isinstance(widget, QtW.QWidget)]

    close_tests(main_window, qtbot)


def check_font_size(widget: QtW.QWidget | QtG.QAction, size: int):
    font = widget.font()
    assert font.pointSize() == size
