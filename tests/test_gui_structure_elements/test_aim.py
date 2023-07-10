from ..starting_closing_tests import start_tests


def test_aim(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    main_window = start_tests(qtbot)
    if not main_window.gui_structure.aim_plot.widget.isChecked():
        main_window.gui_structure.aim_plot.widget.click()

    assert main_window.gui_structure.aim_plot.widget.isChecked()

    main_window.gui_structure.aim_plot.set_text("Hello")
    assert main_window.gui_structure.aim_plot.widget.text() == "Hello"
