import numpy as np

from ScenarioGUI.gui_classes.gui_calculation_thread import calculate

from ..starting_closing_tests import close_tests, start_tests


def test_run_multiple_scenarios_no_autosaving(qtbot):  # noqa: PLR0915
    """
    test if the scenario changing is handled correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.remove_previous_calculated_results()
    gs = main_window.gui_structure

    main_window.save_scenario()
    main_window.add_scenario()
    gs.float_b.set_value(102)
    main_window.save_scenario()
    main_window.add_scenario()
    gs.float_b.set_value(104)
    main_window.save_scenario()

    main_window.start_multiple_scenarios_calculation()
    _ = [thread.run() for thread in main_window.threads]

    main_window.change_scenario(0)
    main_window.display_results()
    assert gs.result_text_add.label.text() == "Result: 102.0m"
    main_window.change_scenario(1)
    main_window.display_results()
    assert gs.result_text_add.label.text() == "Result: 104.0m"
    main_window.change_scenario(2)
    main_window.display_results()
    assert gs.result_text_add.label.text() == "Result: 106.0m"
    close_tests(main_window, qtbot)


def test_run_multiple_scenarios_autosaving(qtbot):  # noqa: PLR0915
    """
    test if the scenario changing is handled correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.remove_previous_calculated_results()
    gs = main_window.gui_structure
    gs.option_auto_saving.set_value(1)

    main_window.add_scenario()
    gs.float_b.set_value(102)
    main_window.add_scenario()
    gs.float_b.set_value(104)

    main_window.start_multiple_scenarios_calculation()
    _ = [thread.run() for thread in main_window.threads]

    main_window.change_scenario(0)
    main_window.display_results()
    assert gs.result_text_add.label.text() == "Result: 102.0m"
    main_window.change_scenario(1)
    assert main_window.list_widget_scenario.currentRow() == 1
    assert gs.result_text_add.label.text() == "Result: 104.0m"
    main_window.change_scenario(2)
    main_window.display_results()
    assert gs.result_text_add.label.text() == "Result: 106.0m"
    close_tests(main_window, qtbot)
