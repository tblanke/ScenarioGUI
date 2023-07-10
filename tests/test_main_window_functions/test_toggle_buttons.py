from ..starting_closing_tests import close_tests, start_tests


def test_toggle_buttons(qtbot):
    """
    test toggle buttons behaviour.

    Parameters
    ----------
    qtbot: QtBot

    """
    main_window = start_tests(qtbot)
    main_window.gui_structure.option_auto_saving.set_value(1)
    # no toggle behaviour
    main_window.gui_structure.option_toggle_buttons.set_value(0)
    main_window.save_scenario()
    main_window.gui_structure.aim_sub.widget.click()
    val_before = main_window.gui_structure.aim_sub.widget.isChecked()
    main_window.gui_structure.aim_sub.widget.click()
    val_after = main_window.gui_structure.aim_sub.widget.isChecked()
    assert val_after == val_before
    main_window.gui_structure.aim_plot.widget.click()
    assert main_window.gui_structure.aim_plot.widget.isChecked()
    assert not main_window.gui_structure.aim_sub.widget.isChecked()

    val_before = main_window.gui_structure.button_box.get_value()
    main_window.gui_structure.button_box.widget[val_before].click()
    val_after = main_window.gui_structure.button_box.get_value()
    assert val_before == val_after
    main_window.gui_structure.button_box.widget[val_before + 1].click()
    val_after = main_window.gui_structure.button_box.get_value()
    assert val_before + 1 == val_after
    # toggle behaviour
    main_window.gui_structure.option_toggle_buttons.set_value(1)
    main_window.save_scenario()
    val_before = main_window.gui_structure.aim_sub.widget.isChecked()
    main_window.gui_structure.aim_sub.widget.click()
    val_after = main_window.gui_structure.aim_sub.widget.isChecked()
    assert val_after != val_before
    main_window.gui_structure.aim_add.widget.click()
    assert main_window.gui_structure.aim_add.widget.isChecked()
    assert not main_window.gui_structure.aim_sub.widget.isChecked()

    val_before = main_window.gui_structure.button_box.get_value()
    main_window.gui_structure.button_box.widget[val_before].click()
    val_after = main_window.gui_structure.button_box.get_value()
    assert main_window.gui_structure.button_box.default_value == val_after
    main_window.gui_structure.button_box.widget[val_before].click()
    val_after = main_window.gui_structure.button_box.get_value()
    assert val_before == val_after
    close_tests(main_window, qtbot)
