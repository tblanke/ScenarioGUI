import PySide6.QtWidgets as QtW
import numpy as np

from ..starting_closing_tests import close_tests, start_tests


def test_value_hint(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    assert np.isclose(float(main_window.gui_structure.value_hint.label[1].text()), main_window.gui_structure.int_units.get_value()[0])
    main_window.gui_structure.int_units.set_value(20)
    assert np.isclose(float(main_window.gui_structure.value_hint.label[1].text()), 20)
    main_window.gui_structure.value_hint.set_text("Hello, World")
    assert main_window.gui_structure.value_hint.label[0].text() == "Hello"
    assert main_window.gui_structure.value_hint.label[2].text() == " World"
    main_window.gui_structure.value_hint.show()
    assert not main_window.gui_structure.value_hint.is_hidden()
    main_window.gui_structure.value_hint.hide()
    assert main_window.gui_structure.value_hint.is_hidden()
    assert "ValueHint; Hint: Hello; Warning: True" == main_window.gui_structure.value_hint.__repr__()
    close_tests(main_window, qtbot)
