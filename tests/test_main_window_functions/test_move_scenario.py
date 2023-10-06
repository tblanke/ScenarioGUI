import numpy as np
import PySide6.QtCore as QtC

from ..starting_closing_tests import close_tests, start_tests


def test_move_scenario_upwards(qtbot):
    """
    test if the change of a scenario works correctly.\n

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    # add three scenarios
    for i in range(1, 6):
        main_window.gui_structure.float_b.set_value(i)
        main_window.save_scenario()
        main_window.add_scenario()
    # save old lists of data storages and names
    li_before = main_window.list_ds.copy()
    li_names_before = [main_window.list_widget_scenario.item(idx).text() for idx in range(main_window.list_widget_scenario.count())]
    # change the items
    main_window.list_widget_scenario.model().moveRow(QtC.QModelIndex(), 1, QtC.QModelIndex(), 3)

    # create check lists by hand from before lists
    li_check = [li_before[0], li_before[2], li_before[1], li_before[3], li_before[4], li_before[5]]
    li_names_check = [li_names_before[0], li_names_before[2], li_names_before[1], li_names_before[3], li_names_before[4], li_names_before[5]]
    for i in range(len(li_check)):
        main_window.list_widget_scenario.setCurrentRow(i)
    # get new lists of data storages and names
    li_after = main_window.list_ds
    li_names_after = [main_window.list_widget_scenario.item(idx).text() for idx in range(main_window.list_widget_scenario.count())]
    # check if names and data storages have been changed correctly
    assert li_names_after == li_names_check
    for ds_old, ds_new in zip(li_after, li_check):
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue
    close_tests(main_window, qtbot)


def test_move_scenario_downwards(qtbot):
    """
    test if the change of a scenario works correctly.\n

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    # add three scenarios
    for i in range(1, 6):
        main_window.gui_structure.float_b.set_value(i)
        main_window.save_scenario()
        main_window.add_scenario()
    # save old lists of data storages and names
    li_before = main_window.list_ds.copy()
    li_names_before = [main_window.list_widget_scenario.item(idx).text() for idx in range(main_window.list_widget_scenario.count())]
    # change the items
    main_window.list_widget_scenario.model().moveRow(QtC.QModelIndex(), 2, QtC.QModelIndex(), 1)

    # create check lists by hand from before lists
    li_check = [li_before[0], li_before[2], li_before[1], li_before[3], li_before[4], li_before[5]]
    li_names_check = [li_names_before[0], li_names_before[2], li_names_before[1], li_names_before[3], li_names_before[4], li_names_before[5]]
    for i in range(len(li_check)):
        main_window.list_widget_scenario.setCurrentRow(i)
    # get new lists of data storages and names
    li_after = main_window.list_ds
    li_names_after = [main_window.list_widget_scenario.item(idx).text() for idx in range(main_window.list_widget_scenario.count())]
    # check if names and data storages have been changed correctly
    assert li_names_after == li_names_check
    for ds_old, ds_new in zip(li_after, li_check):
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue
    close_tests(main_window, qtbot)
