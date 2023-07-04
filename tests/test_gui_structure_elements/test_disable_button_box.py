import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_disable_button_box(qtbot):
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    g_s = main_window.gui_structure
    g_s.aim_add.widget.click() if not g_s.aim_add.widget.isChecked() else None
    g_s.float_b.set_value(100)
    g_s.int_a.set_value(5)
    assert g_s.button_box.widget[0].isEnabled()
    assert g_s.button_box.widget[1].isEnabled()
    assert g_s.button_box.widget[2].isEnabled()
    g_s.aim_plot.widget.click()
    assert g_s.button_box.widget[0].isEnabled()
    assert g_s.button_box.widget[1].isEnabled()
    assert not g_s.button_box.widget[2].isEnabled()
    g_s.float_b.set_value(40)
    assert g_s.button_box.widget[0].isEnabled()
    assert not g_s.button_box.widget[1].isEnabled()
    assert not g_s.button_box.widget[2].isEnabled()
    g_s.button_box_short.widget[0].click()
    assert g_s.button_box_short.widget[0].isEnabled()
    assert not g_s.button_box_short.widget[1].isEnabled()
    assert g_s.button_box_short.get_value() == 0
    g_s.int_a.set_value(12)
    assert not g_s.button_box.widget[0].isEnabled()
    assert not g_s.button_box.widget[1].isEnabled()
    assert not g_s.button_box.widget[2].isEnabled()
    g_s.int_a.set_value(9)
    assert g_s.button_box.widget[0].isEnabled()
    assert not g_s.button_box.widget[1].isEnabled()
    assert not g_s.button_box.widget[2].isEnabled()
    g_s.float_b.set_value(60)
    assert g_s.button_box.widget[0].isEnabled()
    assert g_s.button_box.widget[1].isEnabled()
    assert not g_s.button_box.widget[2].isEnabled()
    g_s.aim_add.widget.click()
    assert g_s.button_box.widget[0].isEnabled()
    assert g_s.button_box.widget[1].isEnabled()
    assert g_s.button_box.widget[2].isEnabled()
    g_s.button_box.set_value(1)
    g_s.button_box_short.widget[1].click()
    g_s.float_b.set_value(40)
    assert g_s.button_box.widget[0].isEnabled()
    assert not g_s.button_box.widget[1].isEnabled()
    assert g_s.button_box.widget[2].isEnabled()
    assert g_s.button_box.get_value() == 0
    assert g_s.button_box_short.get_value() == 0
    main_window.delete_backup()
    for toggled in [0 , 1]:
        main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
        main_window.gui_structure.option_toggle_buttons.set_value(toggled)
        g_s = main_window.gui_structure
        g_s.button_box.set_value(1)
        assert not g_s.filename.is_hidden()
        g_s.float_b.set_value(40)
        assert g_s.filename.is_hidden()
        main_window.delete_backup()
