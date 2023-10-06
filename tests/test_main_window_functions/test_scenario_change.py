from math import isclose

import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW

from ..starting_closing_tests import close_tests, start_tests


def test_change_scenario(qtbot):  # noqa: PLR0915
    """
    test if the scenario changing is handled correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
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
    response = QtW.QMessageBox.Cancel

    class NewMessageBox(QtW.QMessageBox):
        def exec(self):
            return response

    QtW.QMessageBox = NewMessageBox

    # test if closing the window is not changing the value and scenario
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    qtbot.wait(100)
    assert isclose(main_window.gui_structure.float_b.get_value(), 2.3)
    assert main_window.list_widget_scenario.currentRow() == 0
    # test if canceling the window is not changing the value and scenario
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    qtbot.wait(100)
    assert isclose(main_window.gui_structure.float_b.get_value(), 2.3)
    assert main_window.list_widget_scenario.currentRow() == 0
    # test if exiting the window is rejecting the changed the value and changing the scenario
    response = QtW.QMessageBox.Close
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    assert isclose(main_window.gui_structure.float_b.get_value(), 1.1)
    assert isclose(main_window.list_ds[0].float_b, 2.1)
    assert main_window.list_widget_scenario.currentRow() == 1
    # change a value to trigger pop up window
    main_window.gui_structure.float_b.set_value(3)
    # test if saving is saving the changed the value and changing the scenario
    response = QtW.QMessageBox.Save
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(0))
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
    qtbot.wait(200)
    assert isclose(main_window.list_ds[0].float_b, 4)
    assert main_window.list_widget_scenario.currentRow() == 1
    # check if nothing is changed when scenarios are switched
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(0))
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))
    assert isclose(main_window.list_ds[0].float_b, 4)
    assert isclose(main_window.list_ds[1].float_b, 3)
    main_window.scenario_is_changed(main_window.list_widget_scenario.item(1), main_window.list_widget_scenario.item(1))
    assert isclose(main_window.list_ds[1].float_b, 3)
    assert isclose(main_window.gui_structure.float_b.get_value(), 3)
    assert main_window.list_widget_scenario.currentRow() == 1
    main_window.change_scenario(0)
    assert main_window.list_widget_scenario.currentRow() == 0
    assert isclose(main_window.gui_structure.float_b.get_value(), 4)
    close_tests(main_window, qtbot)
