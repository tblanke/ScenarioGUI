import PySide6.QtWidgets as QtW
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results


def test_run(qtbot):
    """
    test if the scenario changing is handled correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.remove_previous_calculated_results()
    main_window.status_hide("")
    main_window.add_scenario()
    file = main_window.gui_structure.filename.get_value()
    main_window.gui_structure.filename.set_value("abc")
    main_window.save_scenario()
    assert main_window.list_widget_scenario.currentItem().text()[-1] == "*"
    main_window.start_current_scenario_calculation()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is None
    main_window.start_multiple_scenarios_calculation()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is None
    main_window.gui_structure.filename.set_value(file)

    main_window.gui_structure.aim_add.widget.click()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    with qtbot.waitSignal(main_window.threads[0].any_signal, raising=False):
        QtW.QApplication.processEvents()

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None

    main_window.remove_previous_calculated_results()

    main_window.gui_structure.aim_sub.widget.click()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    with qtbot.waitSignal(main_window.threads[0].any_signal, raising=False):
        QtW.QApplication.processEvents()

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    main_window.start_current_scenario_calculation(False)
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    main_window.start_multiple_scenarios_calculation()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None

    main_window.remove_previous_calculated_results()

    main_window.gui_structure.aim_plot.widget.click()
    assert main_window.gui_structure.aim_plot.widget.isChecked()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    with qtbot.waitSignal(main_window.threads[0].any_signal, raising=False):
        QtW.QApplication.processEvents()

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    item = main_window.list_widget_scenario.currentItem()
    main_window.add_scenario()
    main_window.gui_structure.int_a.set_value(main_window.gui_structure.int_a.get_value() + 5)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    with qtbot.waitSignal(main_window.threads[0].any_signal, raising=False):
        QtW.QApplication.processEvents()

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    main_window.list_widget_scenario.setCurrentItem(item)
    main_window.display_results()
    main_window.gui_structure.legend_figure_results.set_value(("", 1))

    main_window.remove_previous_calculated_results()
    # test value error results
    main_window.gui_structure.aim_sub.widget.click()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(True)
    with qtbot.waitSignal(main_window.threads[0].any_signal, raising=False):
        main_window.threads[0].run()
        main_window.threads[0].any_signal.connect(main_window.thread_function)
        main_window.display_results()
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None

    main_window.gui_structure.int_a.set_value(192)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(True)
    with qtbot.waitSignal(main_window.threads[0].any_signal, raising=False):
        main_window.threads[0].run()
        main_window.threads[0].any_signal.connect(main_window.thread_function)
        main_window.display_results()

    assert f"{main_window.list_ds[main_window.list_widget_scenario.currentRow()].debug_message}" == "Value above 190"

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is None

    main_window.remove_previous_calculated_results()
    main_window.delete_backup()
