from __future__ import annotations
import os
from pathlib import Path

import PySide6.QtWidgets as QtW
import numpy as np
from matplotlib.backends import qt_compat

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
    while main_window.threads[0].isRunning():
        qtbot.wait(100)
    qtbot.wait(100)
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

    folder = Path(__file__).parent.parent
    file = f'{folder.joinpath("./image.png")}'

    def func(*args) -> tuple[str, str]:
        """get save filename replacement"""
        return file, ".png"

    qt_compat._getSaveFileName = func
    main_window.gui_structure.figure_results_with_different_other_saved_figure.toolbar.save_figure()
    os.remove(main_window.default_path.joinpath(file))

    main_window.gui_structure.figure_results.toolbar.save_figure()
    os.remove(main_window.default_path.joinpath(file))

    main_window.display_results()
    size = main_window.window().size()
    main_window.window().resize(size.width() + 100, size.height() + 150)
    main_window.gui_structure.figure_results.update_figure_layout(None)

    main_window.gui_structure.legend_figure_results.set_value(("", 1))
    main_window.gui_structure.figure_results_with_customizable_layout.change_font()

    main_window.display_results()
    main_window.gui_structure.figure_results_with_customizable_layout.change_font()

    main_window.gui_structure.figure_results_with_customizable_layout.option_figure_background.set_value((100, 110, 111))
    main_window.gui_structure.figure_results_with_customizable_layout.option_plot_background.set_value((101, 111, 112))
    main_window.gui_structure.figure_results_with_customizable_layout.option_axes_text.set_value((99, 113, 115))
    main_window.gui_structure.figure_results_with_customizable_layout.option_axes.set_value((89, 90, 91))
    main_window.gui_structure.figure_results_with_customizable_layout.option_font.set_value(3)
    main_window.gui_structure.figure_results_with_customizable_layout.option_font_size.set_value(15)
    main_window.gui_structure.figure_results_with_customizable_layout.option_legend_text.set_value((120, 121, 122))
    main_window.gui_structure.figure_results_with_customizable_layout.option_title.set_value((130, 131, 132))
    assert not np.allclose(main_window.gui_structure.option_figure_background.get_value(), (100, 110, 111))
    assert not np.allclose(main_window.gui_structure.option_plot_background.get_value(), (100, 110, 111))
    assert not np.allclose(main_window.gui_structure.option_axes_text.get_value(), (100, 110, 111))
    assert not np.allclose(main_window.gui_structure.option_axes.get_value(), (100, 110, 111))
    assert not np.isclose(main_window.gui_structure.option_font.get_value()[0], 3)
    assert not np.isclose(main_window.gui_structure.option_font_size_figure.get_value(), 15)
    assert not np.allclose(main_window.gui_structure.option_legend_text.get_value(), (120, 121, 122))
    assert not np.allclose(main_window.gui_structure.option_title.get_value(), (130, 131, 132))
    main_window.gui_structure.figure_results_with_customizable_layout.option_save_layout.button.click()
    assert np.allclose(main_window.gui_structure.option_figure_background.get_value(), (100, 110, 111))
    assert np.allclose(main_window.gui_structure.option_plot_background.get_value(), (101, 111, 112))
    assert np.allclose(main_window.gui_structure.option_axes_text.get_value(), (99, 113, 115))
    assert np.allclose(main_window.gui_structure.option_axes.get_value(), (89, 90, 91))
    assert np.allclose(main_window.gui_structure.option_font.get_value()[0], 3)
    assert np.isclose(main_window.gui_structure.option_font_size_figure.get_value(), 15)
    assert np.allclose(main_window.gui_structure.option_legend_text.get_value(), (120, 121, 122))
    assert np.allclose(main_window.gui_structure.option_title.get_value(), (130, 131, 132))

    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_figure_background.get_value(), (100, 110, 111))
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_plot_background.get_value(), (101, 111, 112))
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_axes_text.get_value(), (99, 113, 115))
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_axes.get_value(), (89, 90, 91))
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_font.get_value()[0], 3)
    assert np.isclose(main_window.gui_structure.figure_results_with_customizable_layout.option_font_size.get_value(), 15)
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_legend_text.get_value(), (120, 121, 122))
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_title.get_value(), (130, 131, 132))

    main_window.gui_structure.option_figure_background.set_value((16, 17, 18))
    main_window.gui_structure.option_plot_background.set_value((13, 14, 15))
    main_window.gui_structure.option_axes_text.set_value((10, 11, 12))
    main_window.gui_structure.option_axes.set_value((7, 8, 9))
    main_window.gui_structure.option_font.set_value(2)
    main_window.gui_structure.option_font_size_figure.set_value(14)
    main_window.gui_structure.option_legend_text.set_value((1, 2, 3))
    main_window.gui_structure.option_title.set_value((4, 5, 6))

    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_figure_background.get_value(), (16, 17, 18))
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_plot_background.get_value(), (13, 14, 15))
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_axes_text.get_value(), (10, 11, 12))
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_axes.get_value(), (7, 8, 9))
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_font.get_value()[0], 2)
    assert np.isclose(main_window.gui_structure.figure_results_with_customizable_layout.option_font_size.get_value(), 14)
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_legend_text.get_value(), (1, 2, 3))
    assert np.allclose(main_window.gui_structure.figure_results_with_customizable_layout.option_title.get_value(), (4, 5, 6))

    main_window.delete_backup()
