from tests.starting_closing_tests import close_tests, start_tests


def test_results_text(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    # get sum
    sum_ab = main_window.gui_structure.int_a.get_value() + main_window.gui_structure.float_b.get_value()
    main_window.gui_structure.result_text_add.set_text("Hello,kW")
    # calc sum from gui
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    qtbot.wait(1500)
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    # check text output
    assert main_window.gui_structure.result_text_add.label.text() == f"Hello{sum_ab}kW"
    close_tests(main_window, qtbot)
