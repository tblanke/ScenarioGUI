import pytest

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning
from ..starting_closing_tests import close_tests, start_tests


def test_function_button(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.res = 0

    # test function call
    def func():
        main_window.res += 5

    main_window.gui_structure.function_button.change_event(func)
    assert main_window.res == 0
    main_window.gui_structure.function_button.button.click()
    assert main_window.res == 5  # noqa: PLR2004
    # test set text
    main_window.gui_structure.function_button.set_text("Hello")
    assert main_window.gui_structure.function_button.button.text() == "Hello"
    # check show and hide function
    main_window.gui_structure.function_button.show()
    assert not main_window.gui_structure.function_button.is_hidden()
    main_window.gui_structure.function_button.hide()
    assert main_window.gui_structure.function_button.is_hidden()

    main_window.gui_structure.float_units.add_link_2_show(main_window.gui_structure.function_button, 0)

    with pytest.warns(ConditionalVisibilityWarning):
        main_window.gui_structure.float_units.add_link_2_show(main_window.gui_structure.function_button, 2)

    close_tests(main_window, qtbot)
