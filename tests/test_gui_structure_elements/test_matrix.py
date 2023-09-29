import numpy as np
import PySide6.QtGui as QtG
import pytest

from ScenarioGUI.gui_classes.gui_structure_classes import MatrixBox
from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning

from ..starting_closing_tests import close_tests, start_tests


def test_matrix_box(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    matrix: MatrixBox = main_window.gui_structure.matrix
    assert np.allclose(matrix.get_value(), matrix.default_value)

    assert matrix.frame.layout().itemAtPosition(2, 2).widget().maximumWidth() == 100
    assert matrix.frame.layout().itemAtPosition(2, 2).widget().minimumWidth() == 100

    matrix.set_value((np.array(matrix.default_value) + 50).tolist())
    assert np.allclose((np.array(matrix.default_value) + 50).tolist(), matrix.get_value())

    assert matrix.check_linked_value(([[200] * 4] * 3, None))
    assert matrix.check_linked_value((None, [[50] * 4] * 3))
    assert matrix.create_function_2_check_linked_value((None, [[50] * 4] * 3))() == matrix.check_linked_value((None, [[50] * 4] * 3))
    matrix.hide()
    assert matrix.create_function_2_check_linked_value((None, [[50] * 4] * 3), value_if_hidden=True)()
    assert not matrix.create_function_2_check_linked_value((None, [[50] * 4] * 3), value_if_hidden=False)()
    matrix.show()
    assert not matrix.is_hidden()
    assert matrix.create_function_2_check_linked_value((None, [[50] * 4] * 3), value_if_hidden=True)() == matrix.check_linked_value((None, [[50] * 4] * 3))
    matrix.hide()
    matrix.value_if_hidden = True
    assert matrix.create_function_2_check_linked_value((None, [[50] * 4] * 3))()
    matrix.value_if_hidden = False
    assert not matrix.create_function_2_check_linked_value((None, [[50] * 4] * 3))()
    matrix.show()
    assert not matrix.check_linked_value(([[50] * 4] * 3, [[200] * 4] * 3))
    matrix.show_option(main_window.gui_structure.float_units, [[50] * 4] * 3, [[200] * 4] * 3)
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.float_units.is_hidden()
    matrix.set_value([[20] * 4] * 3)
    matrix.show_option(main_window.gui_structure.float_units, [[50] * 4] * 3, [[200] * 4] * 3)
    assert not main_window.gui_structure.float_units.is_hidden()
    matrix.set_value([[220] * 4] * 3)
    matrix.show_option(main_window.gui_structure.float_units, [[50] * 4] * 3, [[200] * 4] * 3)
    assert not main_window.gui_structure.float_units.is_hidden()
    matrix.add_link_2_show(main_window.gui_structure.float_units, [[50] * 4] * 3, [[200] * 4] * 3)
    matrix.set_value([[110] * 4] * 3)
    assert main_window.gui_structure.float_units.is_hidden()
    matrix.set_value([[20] * 4] * 3)
    assert not main_window.gui_structure.float_units.is_hidden()
    matrix.set_value([[220] * 4] * 3)
    assert not main_window.gui_structure.float_units.is_hidden()
    # test set text
    main_window.gui_structure.float_b.set_text("Hello")
    assert main_window.gui_structure.float_b.label.text() == "Hello"
    main_window.save_scenario()
    assert "float_b" in main_window.list_ds[0].to_dict()

    matrix.add_link_2_show(main_window.gui_structure.filename, [[0] * 4] * 3)

    with pytest.warns(ConditionalVisibilityWarning):
        matrix.add_link_2_show(main_window.gui_structure.filename, [[2] * 4] * 3)

    close_tests(main_window, qtbot)
