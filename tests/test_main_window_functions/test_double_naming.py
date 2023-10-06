from ..starting_closing_tests import close_tests, start_tests


def test_gui_scenario_double_naming(qtbot):
    """
    test if two scenarios can have the same name.

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    # create two scenarios
    main_window.add_scenario()
    assert ["Scenario: 1", "Scenario: 2"] == [
        main_window.list_widget_scenario.item(x).text().split("*")[0] for x in range(main_window.list_widget_scenario.count())
    ]
    main_window.list_widget_scenario.setCurrentRow(0)
    main_window.delete_scenario()
    # scenarios are renamed
    assert ["Scenario: 2"] == [main_window.list_widget_scenario.item(x).text().split("*")[0] for x in range(main_window.list_widget_scenario.count())]
    # add two scenarios and check if the second one is named correctly
    main_window.add_scenario()
    main_window.add_scenario()
    assert ["Scenario: 2", "Scenario: 2(2)", "Scenario: 3"] == [
        main_window.list_widget_scenario.item(x).text().split("*")[0] for x in range(main_window.list_widget_scenario.count())
    ]
    # check if this also works with renaming a scenario
    main_window.list_widget_scenario.setCurrentRow(1)
    main_window.fun_rename_scenario("Scenario: 3")
    assert ["Scenario: 2", "Scenario: 3(2)", "Scenario: 3"] == [
        main_window.list_widget_scenario.item(x).text().split("*")[0] for x in range(main_window.list_widget_scenario.count())
    ]
    close_tests(main_window, qtbot)
