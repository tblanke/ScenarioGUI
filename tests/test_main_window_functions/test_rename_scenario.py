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
    main_window.add_scenario()
    # set scenario names
    scenario_name = "test_name"
    scenario_name_2 = "test_name_2"

    # create functions to handle pop up dialog windows to change names, close and reject the dialog

    def change_name():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QInputDialog):
            main_window.dialog.setTextValue(scenario_name)
            main_window.dialog.accept()

    def change_name_2():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QInputDialog):
            main_window.dialog.setTextValue(scenario_name_2)
            main_window.dialog.accept()

    def not_change_name():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QInputDialog):
            main_window.dialog.setTextValue("")
            main_window.dialog.accept()

    def close_dialog():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QInputDialog):
            main_window.dialog.close()

    def reject_dialog():
        while main_window.dialog is None:  # pragma: no cover
            QtW.QApplication.processEvents()
        # handle dialog now
        if isinstance(main_window.dialog, QtW.QInputDialog):
            main_window.dialog.reject()

    # get old item name
    old_name = main_window.list_widget_scenario.item(0).text()
    # enter nothing in the text box and not change the name
    QtC.QTimer.singleShot(100, not_change_name)
    qtbot.mouseClick(main_window.button_rename_scenario, QtC.Qt.MouseButton.LeftButton, delay=1)
    # check if the name stays the old one
    assert main_window.list_widget_scenario.item(0).text() == old_name
    # just close the dialog window
    QtC.QTimer.singleShot(100, close_dialog)
    qtbot.mouseClick(main_window.button_rename_scenario, QtC.Qt.MouseButton.LeftButton, delay=1)
    # check if the name stays the old one
    assert main_window.list_widget_scenario.item(0).text() == old_name
    # abort the dialog window by button
    QtC.QTimer.singleShot(100, reject_dialog)
    qtbot.mouseClick(main_window.button_rename_scenario, QtC.Qt.MouseButton.LeftButton, delay=1)
    # check if the name stays the old one
    assert main_window.list_widget_scenario.item(0).text() == old_name
    # change the name
    QtC.QTimer.singleShot(100, change_name)
    qtbot.mouseClick(main_window.button_rename_scenario, QtC.Qt.MouseButton.LeftButton, delay=1)
    # check the name has been changed correctly
    assert main_window.list_widget_scenario.item(0).text() == scenario_name
    # check if the name can be changed by double click
    QtC.QTimer.singleShot(100, change_name_2)
    main_window.list_widget_scenario.doubleClicked.emit(main_window.list_widget_scenario.model().index(0, 0))
    # check the name has been changed correctly
    assert main_window.list_widget_scenario.item(0).text() == scenario_name_2
    close_tests(main_window, qtbot)
