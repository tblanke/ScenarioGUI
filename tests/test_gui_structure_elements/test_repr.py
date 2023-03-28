import PySide6.QtWidgets as QtW

from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations


def test_repr(qtbot):
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    # assert main_window.gui_structure.figure_temperature_profile.__repr__() == "ResultFigure; Label: Temperature evolution"
    assert main_window.gui_structure.category_inputs.__repr__() == "Category; Label: Inputs"
    assert main_window.gui_structure.option_toggle_buttons.__repr__() == "ButtonBox; Label: Use toggle buttons?:, no , yes ; Value: 1"
    assert main_window.gui_structure.hint_1.__repr__() == "Hint; Hint: Grid example; Warning: False"
    assert main_window.gui_structure.float_b.__repr__() == "FloatBox; Label: b; Value: 100.0"
    assert main_window.gui_structure.int_a.__repr__() == "IntBox; Label: a; Value: 2"
    # assert main_window.gui_structure.legend_figure_temperature_profile.__repr__() == "FigureOption; Label: Show legend?; Value: ('legend', False)"
    main_window.delete_backup()
