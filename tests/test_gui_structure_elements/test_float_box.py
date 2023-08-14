import numpy as np
import PySide6.QtGui as QtG

from ..starting_closing_tests import close_tests, start_tests


def test_float_box(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    float_b = main_window.gui_structure.float_b
    assert np.isclose(float_b.get_value(), float_b.default_value)
    float_b.set_value(float_b.default_value + 50)
    assert np.isclose(float_b.default_value + 50, float_b.get_value())

    assert float_b.check_linked_value((200, None))
    assert float_b.check_linked_value((None, 50))
    assert float_b.create_function_2_check_linked_value((None, 50))() == float_b.check_linked_value((None, 50))
    float_b.hide()
    assert float_b.create_function_2_check_linked_value((None, 50), value_if_hidden=True)()
    assert not float_b.create_function_2_check_linked_value((None, 50), value_if_hidden=False)()
    float_b.show()
    assert not float_b.is_hidden()
    assert float_b.create_function_2_check_linked_value((None, 50), value_if_hidden=True)() == float_b.check_linked_value((None, 50))
    float_b.hide()
    float_b.value_if_hidden = True
    assert float_b.create_function_2_check_linked_value((None, 50))()
    float_b.value_if_hidden = False
    assert not float_b.create_function_2_check_linked_value((None, 50))()
    float_b.show()
    assert not float_b.check_linked_value((50, 200))
    float_b.show_option(main_window.gui_structure.int_a, 50, 200)
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.int_a.is_hidden()
    float_b.set_value(20)
    float_b.show_option(main_window.gui_structure.int_a, 50, 200)
    assert not main_window.gui_structure.int_a.is_hidden()
    float_b.set_value(220)
    float_b.show_option(main_window.gui_structure.int_a, 50, 200)
    assert not main_window.gui_structure.int_a.is_hidden()
    float_b.add_link_2_show(main_window.gui_structure.int_a, 50, 200)
    float_b.set_value(110)
    assert main_window.gui_structure.int_a.is_hidden()
    float_b.set_value(20)
    assert not main_window.gui_structure.int_a.is_hidden()
    float_b.set_value(220)
    assert not main_window.gui_structure.int_a.is_hidden()
    # test validation
    res = float_b.widget.validate("100,020", 5)
    assert np.isclose(float(res[1].replace(",", ".")), 100.02)
    # test set text
    main_window.gui_structure.float_b.set_text("Hello")
    assert main_window.gui_structure.float_b.label.text() == "Hello"
    main_window.save_scenario()
    assert "float_b" in main_window.list_ds[0].to_dict()
    close_tests(main_window, qtbot)
