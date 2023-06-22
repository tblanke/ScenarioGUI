import PySide6.QtWidgets as QtW
import numpy as np

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
    # get sum
    main_window.gui_structure.figure_results.set_text("Hello,Y-Values,X-Values")
    # calc sum from gui
    main_window.save_scenario()
    main_window.start_current_scenario_calculation(False)
    qtbot.wait(1500)
    assert main_window.list_ds[main_window.list_widget_scenario.currentRow()].results is not None
    # check text output
    assert main_window.gui_structure.figure_results.label.text() == "Hello"
    assert main_window.gui_structure.figure_results.a_x.get_ylabel() == "Y-Values"
    assert main_window.gui_structure.figure_results.a_x.get_xlabel() == "X-Values"
    # test scrolling
    main_window.gui_structure.figure_results.scroll_area = ScrollArea()
    val_before = main_window.gui_structure.figure_results.scroll_area.verticalScrollBar().value()
    main_window.gui_structure.figure_results.scrolling(Event("down"))
    val_after = main_window.gui_structure.figure_results.scroll_area.verticalScrollBar().value()
    assert val_after == val_before + 10
    main_window.gui_structure.figure_results.scrolling(Event("up"))
    val_after = main_window.gui_structure.figure_results.scroll_area.verticalScrollBar().value()
    assert val_after == val_before

    main_window.display_results()

    main_window.gui_structure.legend_figure_results.set_value(("", 1))
    main_window.gui_structure.figure_results.change_font()

    main_window.display_results()
    main_window.gui_structure.figure_results.change_font()

    main_window.gui_structure.figure_results.option_figure_background.set_value((100, 110, 111))
    main_window.gui_structure.figure_results.option_plot_background.set_value((101, 111, 112))
    main_window.gui_structure.figure_results.option_axes_text.set_value((99, 113, 115))
    main_window.gui_structure.figure_results.option_axes.set_value((89, 90, 91))
    main_window.gui_structure.figure_results.option_font.set_value(3)
    main_window.gui_structure.figure_results.option_font_size.set_value(15)
    main_window.gui_structure.figure_results.option_legend_text.set_value((120, 121, 122))
    main_window.gui_structure.figure_results.option_title.set_value((130, 131, 132))
    assert not np.allclose(main_window.gui_structure.option_figure_background.get_value(), (100, 110, 111))
    assert not np.allclose(main_window.gui_structure.option_plot_background.get_value(), (100, 110, 111))
    assert not np.allclose(main_window.gui_structure.option_axes_text.get_value(), (100, 110, 111))
    assert not np.allclose(main_window.gui_structure.option_axes.get_value(), (100, 110, 111))
    assert not np.isclose(main_window.gui_structure.option_font.get_value()[0], 3)
    assert not np.isclose(main_window.gui_structure.option_font_size_figure.get_value(), 15)
    assert not np.allclose(main_window.gui_structure.option_legend_text.get_value(), (120, 121, 122))
    assert not np.allclose(main_window.gui_structure.option_title.get_value(), (130, 131, 132))
    main_window.gui_structure.figure_results.option_save_layout.button.click()
    assert np.allclose(main_window.gui_structure.option_figure_background.get_value(), (100, 110, 111))
    assert np.allclose(main_window.gui_structure.option_plot_background.get_value(), (101, 111, 112))
    assert np.allclose(main_window.gui_structure.option_axes_text.get_value(), (99, 113, 115))
    assert np.allclose(main_window.gui_structure.option_axes.get_value(), (89, 90, 91))
    assert np.allclose(main_window.gui_structure.option_font.get_value()[0], 3)
    assert np.isclose(main_window.gui_structure.option_font_size_figure.get_value(), 15)
    assert np.allclose(main_window.gui_structure.option_legend_text.get_value(), (120, 121, 122))
    assert np.allclose(main_window.gui_structure.option_title.get_value(), (130, 131, 132))
    main_window.delete_backup()
