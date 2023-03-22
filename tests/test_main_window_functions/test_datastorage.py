import PySide6.QtWidgets as QtW
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results


def test_datastorage(qtbot):
    """
    tests the datastorage
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.save_scenario()
    main_window.add_scenario()
    assert main_window.list_ds[0] != 2
    assert main_window.list_ds[0] == main_window.list_ds[1]
    val_old = main_window.list_ds[1].float_b
    main_window.list_ds[1].float_b = 1
    assert main_window.list_ds[1] != main_window.list_ds[0]
    main_window.list_ds[1].float_b = val_old
    assert main_window.list_ds[0] == main_window.list_ds[1]
    main_window.list_ds[1].list_options_aims.append("no_real_option")
    assert main_window.list_ds[1] != main_window.list_ds[0]
    main_window.delete_backup()
