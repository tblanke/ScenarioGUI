import pytest

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning
from ..starting_closing_tests import close_tests, start_tests


def test_text_box(qtbot):
    """
    test text box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)

    assert main_window.gui_structure.text_box.get_value() == main_window.gui_structure.text_box.default_value
    main_window.gui_structure.text_box.set_value("Hello")
    assert main_window.gui_structure.text_box.get_value() == "Hello"

    assert main_window.gui_structure.text_box.check_linked_value("Hello")
    assert main_window.gui_structure.text_box.create_function_2_check_linked_value("Hello")() == main_window.gui_structure.text_box.check_linked_value("Hello")

    # test set text
    main_window.gui_structure.text_box.set_text("Hello")
    assert main_window.gui_structure.text_box.label.text() == "Hello"

    main_window.save_scenario()
    assert "text_box" in main_window.list_ds[0].to_dict()

    main_window.gui_structure.text_box.add_link_2_show(main_window.gui_structure.hint_1, "0")

    with pytest.warns(ConditionalVisibilityWarning):
        main_window.gui_structure.text_box.add_link_2_show(main_window.gui_structure.hint_1, "2")

    close_tests(main_window, qtbot)
