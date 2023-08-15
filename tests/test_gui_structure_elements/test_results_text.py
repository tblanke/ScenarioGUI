from tests.starting_closing_tests import close_tests, start_tests


def test_results_text(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    # get sum
    sum_ab = main_window.gui_structure.int_a.get_value() + main_window.gui_structure.float_b.get_value()
    main_window.gui_structure.result_text_add.set_text("Hello,kW")

    main_window.gui_structure.show_option_under_multiple_conditions(
        main_window.gui_structure.result_text_add2,
        [main_window.gui_structure.aim_add, main_window.gui_structure.float_b],
        functions_check_for_and=[
            main_window.gui_structure.aim_add.widget.isChecked,
            main_window.gui_structure.float_b.create_function_2_check_linked_value((main_window.gui_structure.float_b.get_value()-1, None)),
        ],
    )
    main_window.gui_structure.show_option_under_multiple_conditions(
        main_window.gui_structure.result_text_add3,
        [main_window.gui_structure.aim_add, main_window.gui_structure.float_b],
        functions_check_for_and=[
            main_window.gui_structure.aim_add.widget.isChecked,
            main_window.gui_structure.float_b.create_function_2_check_linked_value((main_window.gui_structure.float_b.get_value()+1, None)),
        ],
    )

    # calc sum from gui
    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    assert main_window.gui_structure.result_text_add2.is_hidden()
    assert not main_window.gui_structure.result_text_add3.is_hidden()
    main_window.gui_structure.numerical_results.hide()
    assert main_window.gui_structure.result_text_add2.is_hidden()
    assert not main_window.gui_structure.result_text_add3.is_hidden()
    # check text output
    assert main_window.gui_structure.result_text_add.label.text() == f"Hello{sum_ab}kW"
    close_tests(main_window, qtbot)
