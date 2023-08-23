from typing import TYPE_CHECKING

import numpy as np
from pytest import raises, warns

import ScenarioGUI.global_settings as global_vars
from ScenarioGUI import elements as els
from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning

from ..result_creating_class_for_tests import ResultsClass, data_2_results
from ..starting_closing_tests import close_tests, start_tests

if TYPE_CHECKING:
    from ScenarioGUI.gui_classes.gui_structure_classes.flexible_amount_option import FlexibleAmount

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_flex_amount_option(qtbot):  # noqa: PLR0915
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    flex_option = main_window.gui_structure.flex_option
    flex_option.add_link_2_show(main_window.gui_structure.hint_flex, 4, 12)
    assert len(flex_option.get_value()) == flex_option.default_value
    for li_org, li_val in zip(flex_option.get_value(), flex_option.default_values):
        for org, val in zip(li_org, li_val):
            if isinstance(org, float):
                assert np.isclose(org, val)
                continue
            if isinstance(org, tuple):
                assert org[0] == val
                continue
            assert org == val

    with raises(ValueError):
        flex_option = els.FlexibleAmount(
            label="Test",
            default_length=3,
            entry_mame="Layer",
            category=main_window.gui_structure.category_inputs,
            min_length=5,
            max_length=2,
            default_values=[["layer 1", 9.5, 3, 2], ["layer 2", 10.5, 2, 1]],
        )
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
    flex_option._add_entry_at_row(row=0)
    values = flex_option.get_value()
    assert len(values) == 4  # noqa: PLR2004
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
    assert len(values) == 3  # noqa: PLR2004
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 5, flex_option.frame.layout().itemAtPosition(1, 3).widget().value())
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 10, flex_option.frame.layout().itemAtPosition(2, 3).widget().value())
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 15, flex_option.frame.layout().itemAtPosition(3, 3).widget().value())

    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 5, values[0][1])
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 10, values[1][1])
    assert np.isclose(flex_option.option_classes[1][1]["default_value"] + 15, values[2][1])

    assert not flex_option.check_linked_value((2, None))
    assert not flex_option.check_linked_value((None, 20))
    assert flex_option.check_linked_value((4, 20))
    assert flex_option.check_linked_value((None, 2))
    assert flex_option.check_linked_value((4, 20)) == flex_option.create_function_2_check_linked_value((4, 20))()
    main_window.gui_structure.page_inputs.button.click()

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

    main_window.save_scenario()
    assert "flex_option" in main_window.list_ds[0].to_dict()

    flex_option.hide()
    assert flex_option.frame.isHidden()
    assert flex_option.label.isHidden()
    flex_option.show()
    assert not flex_option.frame.isHidden()
    assert not flex_option.label.isHidden()
    close_tests(main_window, qtbot)

    min_max: FlexibleAmount = main_window.gui_structure.flex_option_min_max
    assert len(min_max.option_entries) == 2  # noqa: PLR2004
    min_max._del_entry(row=1)
    assert len(min_max.option_entries) == 2  # noqa: PLR2004
    min_max._add_entry_at_row(row=0)
    assert len(min_max.option_entries) == 3  # noqa: PLR2004
    min_max._del_entry(row=1)
    assert len(min_max.option_entries) == 2  # noqa: PLR2004
    min_max._add_entry_at_row(row=0)
    min_max._add_entry_at_row(row=0)
    min_max._add_entry_at_row(row=0)
    min_max._add_entry_at_row(row=0)
    min_max._add_entry_at_row(row=0)
    min_max._add_entry_at_row(row=0)
    assert len(min_max.option_entries) == 5  # noqa: PLR2004
    min_max._del_entry(row=0)
    assert len(min_max.option_entries) == 4  # noqa: PLR2004

    min_max.add_link_2_show(main_window.gui_structure.float_b, 1)

    with warns(ConditionalVisibilityWarning):
        min_max.add_link_2_show(main_window.gui_structure.float_b, 0)

    close_tests(main_window, qtbot)
