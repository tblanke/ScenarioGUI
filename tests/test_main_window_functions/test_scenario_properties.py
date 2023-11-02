from ..starting_closing_tests import close_tests, start_tests


def test_gui_scenario_properties(qtbot):
    """
    test if gui scenario properties like adding and deleting are working correctly.

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    # check if at start no scenario exists
    assert len(main_window.list_ds) == 1
    assert main_window.list_widget_scenario.count() == 1
    # check if saving of a scenario if an empty list create one
    main_window.save_scenario()
    assert len(main_window.list_ds) == 1
    assert main_window.list_widget_scenario.count() == 1
    # check if adding a scenario is adding one
    for i in range(10):
        main_window.save_scenario()
        main_window.dia.setWindowTitle(main_window.dia.windowTitle()[:-1])
        main_window.changedFile = False
        assert main_window.dia.windowTitle()[-1] != "*"
        main_window.add_scenario()
        assert len(main_window.list_ds) == 2 + i
        assert main_window.list_widget_scenario.count() == 2 + i
        assert main_window.dia.windowTitle()[-1] == "*"
    # check if deleting a scenario is removing a scenario
    for i in range(10):
        main_window.dia.setWindowTitle(main_window.dia.windowTitle()[:-1])
        main_window.changedFile = False
        assert main_window.dia.windowTitle()[-1] != "*"
        main_window.delete_scenario()
        assert len(main_window.list_ds) == 10 - i
        assert main_window.list_widget_scenario.count() == 10 - i
        assert main_window.dia.windowTitle()[-1] == "*"
    # check if deleting the last scenario is ignored so at least one exists
    main_window.delete_scenario()
    assert len(main_window.list_ds) == 1
    assert main_window.list_widget_scenario.count() == 1
    close_tests(main_window, qtbot)
