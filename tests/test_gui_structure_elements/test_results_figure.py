import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from tests.gui_structure_for_tests import GUI
from tests.result_creating_class_for_tests import ResultsClass, data_2_results
from tests.test_translations.translation_class import Translations


class Event:
    def __init__(self, button: str):
        self.button = button


class VerticalBar:

    def __init__(self):
        self.val = 50

    def setValue(self, val: int):
        self.val = val

    def value(self) -> int:
        return self.val

    def singleStep(self) -> int:
        return 10


class ScrollArea:
    def __init__(self):
        self.vertical_bar = VerticalBar()

    def verticalScrollBar(self) -> VerticalBar:
        return self.vertical_bar


def test_results_figure(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.gui_structure.aim_add.add_link_2_show(main_window.gui_structure.figure_results)
    main_window.gui_structure.aim_sub.add_link_2_show(main_window.gui_structure.figure_results)
    # get sum
    main_window.gui_structure.figure_results.set_text("Hello,Y-Values,X-Values,Line 1")
    # calc sum from gui
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    qtbot.wait(1500)
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    main_window.gui_structure.page_result.button.click()
    main_window.gui_structure.legend_figure_results.widget[1].click()
    main_window.display_results()
    # check text output
    assert main_window.gui_structure.figure_results.label.text() == "Hello"
    assert main_window.gui_structure.figure_results.a_x.get_ylabel() == "Y-Values"
    assert main_window.gui_structure.figure_results.a_x.get_xlabel() == "X-Values"
    assert main_window.gui_structure.figure_results.a_x.get_legend().get_texts()[0].get_text() == "Line 1"

    main_window.gui_structure.figure_results.set_text("Hello,Y-Values,X-Values,Line 1")
    # test scrolling
    main_window.gui_structure.figure_results.scroll_area = ScrollArea()
    val_before = main_window.gui_structure.figure_results.scroll_area.verticalScrollBar().value()
    main_window.gui_structure.figure_results.scrolling(Event("down"))
    val_after = main_window.gui_structure.figure_results.scroll_area.verticalScrollBar().value()
    assert val_after == val_before + 10
    main_window.gui_structure.figure_results.scrolling(Event("up"))
    val_after = main_window.gui_structure.figure_results.scroll_area.verticalScrollBar().value()
    assert val_after == val_before
    main_window.delete_backup()
