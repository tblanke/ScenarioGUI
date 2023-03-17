from math import isclose

import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_change_scenario(qtbot):
    """
    test if the scenario changing is handled correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    # add two scenarios and set different conductivity
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(2.1)
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(1.1)
    main_window.save_scenario()
    # change scenario to first one and check for the correct value
    assert main_window.list_widget_scenario.currentRow() == 1
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(0))
    assert isclose(main_window.gui_structure.float_b.get_value(), 2.1)
    assert main_window.list_widget_scenario.currentRow() == 0
    # change a value to trigger pop up window
    main_window.gui_structure.float_b.set_value(2.3)
    # create functions to handle pop up window

    def close():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QMessageBox):
            main_window.dialog.close()

    def abort():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QMessageBox):
            main_window.dialog.buttons()[2].click()

    def exit_window():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QMessageBox):
            main_window.dialog.buttons()[1].click()

    def save():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QMessageBox):
            main_window.dialog.buttons()[0].click()
    # test if closing the window is not changing the value and scenario
    QtC.QTimer.singleShot(100, close)
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    assert isclose(main_window.gui_structure.float_b.get_value(), 2.3)
    qtbot.wait(100)
    assert main_window.list_widget_scenario.currentRow() == 0
    # test if canceling the window is not changing the value and scenario
    QtC.QTimer.singleShot(100, abort)
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    assert isclose(main_window.gui_structure.float_b.get_value(), 2.3)
    qtbot.wait(100)
    assert main_window.list_widget_scenario.currentRow() == 0
    # test if exiting the window is rejecting the changed the value and changing the scenario
    QtC.QTimer.singleShot(100, exit_window)
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    qtbot.wait(100)
    assert isclose(main_window.gui_structure.float_b.get_value(), 1.1)
    assert isclose(main_window.list_ds[0].float_b, 2.1)
    assert main_window.list_widget_scenario.currentRow() == 1
    # change a value to trigger pop up window
    main_window.gui_structure.float_b.set_value(3)
    # test if saving is saving the changed the value and changing the scenario
    QtC.QTimer.singleShot(100, save)
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(0))
    qtbot.wait(100)
    assert isclose(main_window.list_ds[1].float_b, 3)
    assert main_window.list_widget_scenario.currentRow() == 0
    # check if the * is removed when it is changed to old values
    old_value = main_window.gui_structure.float_b.get_value()
    main_window.gui_structure.float_b.set_value(4)
    assert main_window.list_widget_scenario.currentItem().text()[-1] == "*"
    main_window.gui_structure.float_b.set_value(old_value)
    assert main_window.list_widget_scenario.currentItem().text()[-1] != "*"
    # check if just one * is added if multiple options are changed
    main_window.gui_structure.float_b.set_value(4)
    main_window.gui_structure.float_small_1.set_value(4)
    assert main_window.list_widget_scenario.currentItem().text()[-1] == "*"
    assert main_window.list_widget_scenario.currentItem().text()[-2] != "**"
    main_window.save_scenario()
    assert main_window.list_widget_scenario.currentItem().text()[-1] != "*"
    file = main_window.gui_structure.filename.get_value()
    main_window.gui_structure.filename.set_value("abc")
    main_window.save_scenario()
    assert main_window.list_widget_scenario.currentItem().text()[-1] == "*"
    main_window.gui_structure.filename.set_value(file)
    main_window.save_scenario()
    # activate auto saving option
    main_window.gui_structure.option_auto_saving.set_value(1)
    # check if the value is stored and the scenario is changed
    main_window.gui_structure.float_b.set_value(4)
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    qtbot.wait(100)
    assert isclose(main_window.list_ds[0].float_b, 4)
    assert main_window.list_widget_scenario.currentRow() == 1
    # check if nothing is changed when scenarios are switched
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(0))
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    assert isclose(main_window.list_ds[0].float_b, 4)
    assert isclose(main_window.list_ds[1].float_b, 3)
    main_window.delete_backup()
    