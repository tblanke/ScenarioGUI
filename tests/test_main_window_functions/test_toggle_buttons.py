import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_toggle_buttons(qtbot):
    """
    test toggle buttons behaviour.

    Parameters
    ----------
    qtbot: QtBot

    """
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.gui_structure.option_auto_saving.set_value(1)
    # no toggle behaviour
    main_window.gui_structure.option_toggle_buttons.set_value(0)
    main_window.save_scenario()
    main_window.gui_structure.aim_sub.widget.click()
    val_before = main_window.gui_structure.aim_sub.widget.isChecked()
    main_window.gui_structure.aim_sub.widget.click()
    val_after = main_window.gui_structure.aim_sub.widget.isChecked()
    assert val_after == val_before
    main_window.gui_structure.aim_plot.widget.click()
    assert main_window.gui_structure.aim_plot.widget.isChecked()
    assert not main_window.gui_structure.aim_sub.widget.isChecked()

    val_before = main_window.gui_structure.button_box.get_value()
    main_window.gui_structure.button_box.widget[val_before].click()
    val_after = main_window.gui_structure.button_box.get_value()
    assert val_before == val_after
    main_window.gui_structure.button_box.widget[val_before + 1].click()
    val_after = main_window.gui_structure.button_box.get_value()
    assert val_before + 1 == val_after
    # toggle behaviour
    main_window.gui_structure.option_toggle_buttons.set_value(1)
    main_window.save_scenario()
    val_before = main_window.gui_structure.aim_sub.widget.isChecked()
    main_window.gui_structure.aim_sub.widget.click()
    val_after = main_window.gui_structure.aim_sub.widget.isChecked()
    assert val_after != val_before
    main_window.gui_structure.aim_add.widget.click()
    assert main_window.gui_structure.aim_add.widget.isChecked()
    assert not main_window.gui_structure.aim_sub.widget.isChecked()

    val_before = main_window.gui_structure.button_box.get_value()
    main_window.gui_structure.button_box.widget[val_before].click()
    val_after = main_window.gui_structure.button_box.get_value()
    assert main_window.gui_structure.button_box.default_value == val_after
    main_window.gui_structure.button_box.widget[val_before].click()
    val_after = main_window.gui_structure.button_box.get_value()
    assert val_before == val_after
    main_window.delete_backup()
