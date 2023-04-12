import numpy as np
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow

from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..test_translations.translation_class import Translations

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_flex_amount_option(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    main_window.delete_backup()
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    flex_option = main_window.gui_structure.flex_option
    assert len(flex_option.get_value()) == flex_option.default_value
    flex_option._add_entry()
    assert len(flex_option.get_value()) == flex_option.default_value + 1
    flex_option._del_entry()
    assert len(flex_option.get_value()) == flex_option.default_value
    flex_option.set_value([["Name", 1, 2, 0]])
    assert len(flex_option.get_value()) == 1
    flex_option._del_entry()
    assert len(flex_option.get_value()) == 1
    flex_option._add_entry()
    flex_option._add_entry()
    flex_option.frame.layout().itemAtPosition(1, 3).widget().setValue(flex_option.option_classes[1][1]["default_value"] + 5)
    flex_option.frame.layout().itemAtPosition(2, 3).widget().setValue(flex_option.option_classes[1][1]["default_value"] + 10)
    flex_option.frame.layout().itemAtPosition(3, 3).widget().setValue(flex_option.option_classes[1][1]["default_value"] + 15)
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 5, flex_option.frame.layout().itemAtPosition(1, 3).widget().value())
    flex_option._add_entry_at_row(0)
    values = flex_option.get_value()
    assert len(values) == 4
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 5, flex_option.frame.layout().itemAtPosition(1, 3).widget().value())
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 5, flex_option.frame.layout().itemAtPosition(2, 3).widget().value())
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 10, flex_option.frame.layout().itemAtPosition(3, 3).widget().value())
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 15, flex_option.frame.layout().itemAtPosition(4, 3).widget().value())
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 5, values[0][1])
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 5, values[1][1])
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 10, values[2][1])
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 15, values[3][1])
    flex_option._del_entry(row=1)
    values = flex_option.get_value()
    assert len(values) == 3
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 5, flex_option.frame.layout().itemAtPosition(1, 3).widget().value())
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 10, flex_option.frame.layout().itemAtPosition(2, 3).widget().value())
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 15, flex_option.frame.layout().itemAtPosition(3, 3).widget().value())

    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 5, values[0][1])
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 10, values[1][1])
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 15, values[2][1])

    flex_option._init_links()
    assert not flex_option.check_linked_value((2, None))
    assert not flex_option.check_linked_value((None, 20))
    assert flex_option.check_linked_value((4, 20))
    assert flex_option.check_linked_value((None, 2))
    main_window.gui_structure.page_inputs.button.click()
    flex_option._init_links()
    assert not main_window.gui_structure.hint_flex.is_hidden()
    flex_option.set_value([["name", 4, 3, 0] for _ in range(5)])
    assert main_window.gui_structure.hint_flex.is_hidden()
    flex_option.set_value([["name", 4, 3, 0] for _ in range(14)])
    assert not main_window.gui_structure.hint_flex.is_hidden()
    flex_option.set_text("label_text,row,str,float,int,list")
    assert flex_option.label.text() == "label_text"
    assert flex_option.frame.layout().itemAtPosition(1, 0).widget().text() == "row 1"
    assert flex_option.frame.layout().itemAtPosition(0, 2).widget().text() == "str"
    assert flex_option.frame.layout().itemAtPosition(0, 3).widget().text() == "float"
    assert flex_option.frame.layout().itemAtPosition(0, 4).widget().text() == "int"
    assert flex_option.frame.layout().itemAtPosition(0, 5).widget().text() == "list"

    flex_option.hide()
    assert flex_option.frame.isHidden()
    assert flex_option.label.isHidden()
    flex_option.show()
    assert not flex_option.frame.isHidden()
    assert not flex_option.label.isHidden()
    main_window.delete_backup()
