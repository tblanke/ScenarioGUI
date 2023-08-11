from tests.starting_closing_tests import close_tests, start_tests


def test_result_text_on_on_result_page(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    # check if graphics are created
    gs = main_window.gui_structure

    assert not gs.result_text_not_on_result_page.is_hidden()

    main_window.save_scenario()
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[0]
    thread.run()
    assert thread.calculated
    main_window.display_results()
    assert gs.result_text_add.label.text() == "Result: 102.0m"
    close_tests(main_window, qtbot)
