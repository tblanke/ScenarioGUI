import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW

from ..starting_closing_tests import close_tests, start_tests


def test_rename_scenario(qtbot):  # noqa: PLR0915
    """
    test renaming of scenario by button and double click.

    Parameters
    ---------- # noqa: PLR0915
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.fun_rename_scenario("name")
    # set scenario names
    scenario_name = "test_name"
    scenario_name_2 = "test_name_2"
    # create functions to handle pop up dialog windows to change names, close and reject the dialog
    response = QtW.QMessageBox.Cancel
    ret_scenario_name = scenario_name

    class NewQDialog(QtW.QInputDialog):

        def textValue(self) -> str:
            return ret_scenario_name

        def exec(self):
            return response

    QtW.QInputDialog = NewQDialog

    main_window.dia.setWindowTitle(main_window.dia.windowTitle()[:-1])
    main_window.changedFile = False
    assert main_window.dia.windowTitle()[-1] != "*"
    # get old item name
    old_name = main_window.list_widget_scenario.item(0).text()
    # enter nothing in the text box and not change the name
    qtbot.mouseClick(main_window.button_rename_scenario, QtC.Qt.MouseButton.LeftButton, delay=1)
    # check if the name stays the old one
    assert main_window.list_widget_scenario.item(0).text() == old_name
    assert main_window.dia.windowTitle()[-1] != "*"
    # just close the dialog window
    qtbot.mouseClick(main_window.button_rename_scenario, QtC.Qt.MouseButton.LeftButton, delay=1)
    # check if the name stays the old one
    assert main_window.list_widget_scenario.item(0).text() == old_name
    assert main_window.dia.windowTitle()[-1] != "*"
    # abort the dialog window by button
    response = QtW.QMessageBox.Close
    qtbot.mouseClick(main_window.button_rename_scenario, QtC.Qt.MouseButton.LeftButton, delay=1)
    # check if the name stays the old one
    assert main_window.list_widget_scenario.item(0).text() == old_name
    assert main_window.dia.windowTitle()[-1] != "*"
    # change the name
    response = QtW.QDialog.Accepted
    qtbot.mouseClick(main_window.button_rename_scenario, QtC.Qt.MouseButton.LeftButton, delay=1)
    # check the name has been changed correctly
    assert main_window.list_widget_scenario.item(0).text() == scenario_name
    assert main_window.dia.windowTitle()[-1] == "*"
    # check if the name can be changed by double click
    ret_scenario_name = scenario_name_2
    main_window.dia.setWindowTitle(main_window.dia.windowTitle()[:-1])
    main_window.changedFile = False
    assert main_window.dia.windowTitle()[-1] != "*"
    main_window.list_widget_scenario.doubleClicked.emit(main_window.list_widget_scenario.model().index(0, 0))
    # check the name has been changed correctly
    assert main_window.list_widget_scenario.item(0).text() == scenario_name_2
    assert main_window.dia.windowTitle()[-1] == "*"
    close_tests(main_window, qtbot)
