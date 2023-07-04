import PySide6.QtWidgets as QtW
import numpy as np

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


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

    main_window.gui_structure.aim_add.widget.click() if not main_window.gui_structure.aim_add.widget.isChecked() else None
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    qtbot.wait(1500)

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    assert np.isclose(main_window.list_ds[main_window.list_widget_scenario.currentRow()].results.result, 102)
    main_window.list_ds[main_window.list_widget_scenario.currentRow()].results.adding()
    assert np.isclose(main_window.list_ds[main_window.list_widget_scenario.currentRow()].results.result, 102)

    main_window.remove_previous_calculated_results()

    main_window.gui_structure.aim_sub.widget.click()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    qtbot.wait(1500)

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
    qtbot.wait(1500)

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    item = main_window.list_widget_scenario.currentItem()
    main_window.add_scenario()
    main_window.gui_structure.int_a.set_value(main_window.gui_structure.int_a.get_value() + 5)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(True)
    main_window.threads[-1].run()
    main_window.threads[-1].any_signal.connect(main_window.thread_function)
    qtbot.wait(1500)
    main_window.display_results()

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    main_window.list_widget_scenario.setCurrentItem(item)
    main_window.display_results()
    main_window.gui_structure.legend_figure_results_with_customizable_layout.set_value(("", 1))
    main_window.gui_structure.figure_results_with_customizable_layout.change_font()
    main_window.gui_structure.figure_results_with_customizable_layout.a_x.set_title(None)
    main_window.gui_structure.figure_results_with_customizable_layout.change_title_color()

    main_window.remove_previous_calculated_results()
    # test value error results
    main_window.gui_structure.aim_sub.widget.click()
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(True)
    thread = main_window.threads[-1]
    thread.run()
    thread.any_signal.connect(main_window.thread_function)
    qtbot.wait(1500)
    main_window.display_results()

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None

    main_window.gui_structure.int_a.set_value(192)
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(True)
    thread = main_window.threads[-1]
    thread.run()
    thread.any_signal.connect(main_window.thread_function)
    qtbot.wait(1500)
    main_window.display_results()

    assert f"{main_window.list_ds[main_window.list_widget_scenario.currentRow()].debug_message}" == "Value above 190"

    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is None

    main_window.remove_previous_calculated_results()
    main_window.delete_backup()
