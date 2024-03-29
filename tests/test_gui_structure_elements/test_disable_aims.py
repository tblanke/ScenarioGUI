import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_disable_aims(qtbot):
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    g_s = main_window.gui_structure
    g_s.aim_add.widget.click() if not g_s.aim_add.widget.isChecked() else None
    g_s.float_b.set_value(100)
    g_s.int_a.set_value(5)
    g_s.int_units.set_value((10, 0))
    g_s.aim_last.widget.setEnabled(False)
    assert g_s.aim_sub.widget.isEnabled()
    assert g_s.aim_add.widget.isEnabled()
    assert g_s.aim_plot.widget.isEnabled()
    g_s.int_a.set_value(201)
    assert not g_s.aim_sub.widget.isEnabled()
    assert g_s.aim_add.widget.isEnabled()
    assert g_s.aim_plot.widget.isEnabled()
    g_s.float_b.set_value(29)
    assert not g_s.aim_sub.widget.isEnabled()
    assert not g_s.aim_add.widget.isEnabled()
    assert g_s.aim_plot.widget.isEnabled()
    g_s.int_units.set_value((30, 0))
    assert not g_s.aim_sub.widget.isEnabled()
    assert not g_s.aim_add.widget.isEnabled()
    assert not g_s.aim_plot.widget.isEnabled()
    g_s.int_units.set_value((15, 0))
    assert not g_s.aim_sub.widget.isEnabled()
    assert not g_s.aim_add.widget.isEnabled()
    assert g_s.aim_plot.widget.isEnabled()
    g_s.float_b.set_value(60)
    assert not g_s.aim_sub.widget.isEnabled()
    assert g_s.aim_add.widget.isEnabled()
    assert g_s.aim_plot.widget.isEnabled()
    g_s.aim_last.widget.setEnabled(True)
    g_s.int_a.set_value(5)
    assert g_s.aim_sub.widget.isEnabled()
    assert g_s.aim_add.widget.isEnabled()
    assert g_s.aim_plot.widget.isEnabled()
    g_s.aim_sub.widget.click()
    g_s.int_a.set_value(201)
    assert not g_s.aim_sub.widget.isEnabled()
    assert g_s.aim_add.widget.isEnabled()
    assert g_s.aim_plot.widget.isEnabled()
    assert g_s.aim_add.widget.isChecked()
    g_s.int_units.set_value((30, 0))
    g_s.aim_add.widget.click()
    assert g_s.aim_last.widget.isChecked()
    main_window.delete_backup()
    for toggled in [0 , 1]:
        main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
        main_window.gui_structure.aim_add.add_link_2_show(main_window.gui_structure.text_box_only_on_add)
        main_window.gui_structure.option_toggle_buttons.set_value(toggled)
        main_window.gui_structure.aim_sub.widget.click()
        assert main_window.gui_structure.text_box_only_on_add.is_hidden()
        main_window.gui_structure.int_a.set_value(210)
        assert not main_window.gui_structure.text_box_only_on_add.is_hidden()
        main_window.delete_backup()
        main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass,
                                 data_2_results_function=data_2_results)
        main_window.gui_structure.option_toggle_buttons.set_value(toggled)
        main_window.gui_structure.aim_add.widget.click() if not main_window.gui_structure.aim_add.widget.isChecked() else None
        assert not main_window.gui_structure.text_box_only_on_add.is_hidden()
        main_window.gui_structure.int_a.set_value(210)
        assert not main_window.gui_structure.text_box_only_on_add.is_hidden()
        main_window.gui_structure.option_toggle_buttons.set_value(main_window.gui_structure.option_toggle_buttons.default_value)
        main_window.delete_backup()


def test_disable_aim_and_show_under_multiple_conditions(qtbot):
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass,
                             data_2_results_function=data_2_results)
    g_s = main_window.gui_structure
    g_s.aim_sub.widget.click()
    g_s.button_box_short.set_value(1)
    assert g_s.text_box_small.is_hidden()
    g_s.int_a.set_value(600)
    assert g_s.aim_add.is_checked()
    assert not g_s.text_box_small.is_hidden()

    # with toggled disabled
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass,
                             data_2_results_function=data_2_results)
    g_s = main_window.gui_structure
    g_s.option_toggle_buttons.set_value(0)
    g_s.aim_sub.widget.click()
    g_s.button_box_short.set_value(1)
    assert g_s.text_box_small.is_hidden()
    g_s.int_a.set_value(600)
    assert g_s.aim_add.is_checked()
    assert not g_s.text_box_small.is_hidden()