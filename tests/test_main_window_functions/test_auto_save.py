from math import isclose

from ..starting_closing_tests import close_tests, start_tests


def test_auto_save(qtbot):
    """
    test if the auto save function works

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    # set auto save function and create new backup file
    main_window.gui_structure.option_auto_saving.set_value(1)
    main_window.auto_save()
    # add a new scenario and change conductivity
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(2.1)
    # add a new scenario and change conductivity
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(1.1)
    # run calculations
    main_window.action_start_multiple.trigger()
    qtbot.wait(100)
    # check if options has been stored correctly
    assert isclose(main_window.list_ds[1].float_b, 2.1)
    assert isclose(main_window.list_ds[2].float_b, 1.1)
    for _ in main_window.list_ds:
        main_window.delete_scenario()
        qtbot.wait(100)
    assert len(main_window.list_ds) == 1
    assert main_window.list_widget_scenario.count() == 1
    # check if adding a scenario is adding one
    for i in range(10):
        main_window.add_scenario()
        assert len(main_window.list_ds) == 2 + i
        assert main_window.list_widget_scenario.count() == 2 + i
    # check if deleting a scenario is removing a scenario
    for i in range(10):
        main_window.delete_scenario()
        assert len(main_window.list_ds) == 10 - i
        assert main_window.list_widget_scenario.count() == 10 - i
    # check if deleting the last scenario is ignored so at least one exists
    main_window.delete_scenario()
    assert len(main_window.list_ds) == 1
    assert main_window.list_widget_scenario.count() == 1

    main_window.gui_structure.option_auto_saving.set_value(0)
    close_tests(main_window, qtbot)
