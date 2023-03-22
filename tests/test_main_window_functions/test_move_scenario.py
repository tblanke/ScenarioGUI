import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results


def test_move_scenario(qtbot):
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
    # add three scenarios
    main_window.add_scenario()
    main_window.add_scenario()
    main_window.gui_structure.aim_add.widget.click()
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.button_box.set_value(1)
    main_window.save_scenario()
    # save old lists of data storages and names
    li_before = main_window.list_ds.copy()
    li_names_before = [main_window.list_widget_scenario.item(idx).text() for idx in range(main_window.list_widget_scenario.count())]
    # change the items
    main_window.list_widget_scenario.model().moveRow(QtC.QModelIndex(), 2, QtC.QModelIndex(), 0)
    # get new lists of data storages and names
    li_after = main_window.list_ds
    li_names_after = [main_window.list_widget_scenario.item(idx).text() for idx in range(main_window.list_widget_scenario.count())]
    # create check lists by hand from before lists
    li_check = [li_before[2], li_before[0], li_before[1]]
    li_names_check = [li_names_before[2], li_names_before[0], li_names_before[1]]
    # check if names and data storages have been changed correctly
    assert li_after == li_check
    assert li_names_after == li_names_check
    main_window.delete_backup()
