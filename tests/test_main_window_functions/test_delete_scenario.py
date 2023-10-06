import numpy as np

from ..starting_closing_tests import close_tests, start_tests


def test_delete_scenarios(qtbot):
    """
    test if the deleting of scenario is performed correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    # create two scenarios
    main_window.gui_structure.float_b.set_value(1)
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(2)
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(3)
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(4)
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(5)
    main_window.save_scenario()

    assert main_window.list_widget_scenario.currentRow() == 4

    main_window.list_widget_scenario.setCurrentRow(1)

    assert main_window.list_widget_scenario.currentRow() == 1

    main_window.delete_scenario()

    assert main_window.list_widget_scenario.currentRow() == 1
    assert np.isclose(main_window.gui_structure.float_b.get_value(), 3)

    main_window.list_widget_scenario.setCurrentRow(3)

    main_window.delete_scenario()

    assert main_window.list_widget_scenario.currentRow() == 2
    assert np.isclose(main_window.gui_structure.float_b.get_value(), 4)

    main_window.list_widget_scenario.setCurrentRow(1)
    main_window.MOVE_2_NEXT = False

    main_window.delete_scenario()

    assert main_window.list_widget_scenario.currentRow() == 0
    assert np.isclose(main_window.gui_structure.float_b.get_value(), 1)

    main_window.delete_scenario()

    assert main_window.list_widget_scenario.currentRow() == 0
    assert np.isclose(main_window.gui_structure.float_b.get_value(), 4)

    close_tests(main_window, qtbot)
