import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW
import numpy as np

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_move_scenario_upwards(qtbot):
    """
    test if the change of a scenario works correctly.\n

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.add_scenario()
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
    main_window.delete_backup()


def test_move_scenario_downwards(qtbot):
    """
    test if the change of a scenario works correctly.\n

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.add_scenario()
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
    main_window.delete_backup()
    