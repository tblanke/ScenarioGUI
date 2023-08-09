import numpy as np

from ..starting_closing_tests import close_tests, start_tests


def test_run(qtbot):  # noqa: PLR0915
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
    main_window.add_scenario()
    file = main_window.gui_structure.filename.get_value()
    main_window.gui_structure.filename.set_value("abc")
    main_window.save_scenario()
    assert main_window.list_widget_scenario.currentItem().text()[-1] == "*"
    main_window.start_current_scenario_calculation()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is None
    main_window.start_multiple_scenarios_calculation()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is None
    main_window.gui_structure.filename.set_value(file)

    main_window.gui_structure.aim_add.widget.click() if not main_window.gui_structure.aim_add.widget.isChecked() else None
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    main_window.check_results()
    main_window.auto_save()
    thread = main_window.saving_threads[0]
    thread.run()
    assert thread.calculated
    main_window.load_backup()
    assert np.isclose(main_window.list_ds[main_window.list_widget_scenario.currentRow()].results.result, 102)
    main_window.list_ds[main_window.list_widget_scenario.currentRow()].results.adding()
    assert np.isclose(main_window.list_ds[main_window.list_widget_scenario.currentRow()].results.result, 102)

    main_window.remove_previous_calculated_results()

    main_window.gui_structure.aim_sub.widget.click()
    main_window.save_scenario()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is None
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    main_window.start_current_scenario_calculation()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    main_window.start_multiple_scenarios_calculation()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None

    main_window.remove_previous_calculated_results()

    main_window.gui_structure.aim_plot.widget.click()
    assert main_window.gui_structure.aim_plot.widget.isChecked()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    item = main_window.list_widget_scenario.currentItem()
    main_window.add_scenario()
    main_window.gui_structure.int_a.set_value(main_window.gui_structure.int_a.get_value() + 5)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    main_window.display_results()

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    main_window.list_widget_scenario.setCurrentItem(item)
    main_window.display_results()
    main_window.gui_structure.legend_figure_results_with_customizable_layout.set_value(("", 1))
    main_window.gui_structure.figure_results_with_customizable_layout.change_font()
    main_window.gui_structure.figure_results_with_customizable_layout.a_x.set_title(None)
    main_window.gui_structure.figure_results_with_customizable_layout.change_title_color()

    main_window.remove_previous_calculated_results()
    # test value error results
    main_window.gui_structure.aim_sub.widget.click()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    main_window.display_results()

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None

    main_window.gui_structure.int_a.set_value(192)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    main_window.display_results()

    assert f"{main_window.list_ds[main_window.list_widget_scenario.currentRow()].debug_message}" == "Value above 190"

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is None

    main_window.remove_previous_calculated_results()
    close_tests(main_window, qtbot)


def test_max_run_time(qtbot):
    """
    test if maximal runtime error is occurring

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.remove_previous_calculated_results()
    main_window.add_scenario()
    file = main_window.gui_structure.filename.get_value()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is None
    main_window.gui_structure.filename.set_value(file)
    main_window.gui_structure.time_out.set_value(1)

    main_window.gui_structure.aim_sub.widget.click() if not main_window.gui_structure.aim_sub.widget.isChecked() else None
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is None
    assert "run time" in main_window.gui_structure.text_no_result.label.text()