import pytest

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning
from ..starting_closing_tests import close_tests, start_tests


def test_multiline_text_box(qtbot):
    """
    test text box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)

    assert main_window.gui_structure.text_box_multi_line.get_value() == main_window.gui_structure.text_box_multi_line.default_value
    main_window.gui_structure.text_box_multi_line.set_value("Hello\nWorld")
    assert main_window.gui_structure.text_box_multi_line.get_value() == "Hello\nWorld"

    assert main_window.gui_structure.text_box_multi_line.check_linked_value("Hello\nWorld")
    assert main_window.gui_structure.text_box_multi_line.create_function_2_check_linked_value(
        "Hello\nWorld"
    )() == main_window.gui_structure.text_box_multi_line.check_linked_value("Hello\nWorld")

    # test set text
    main_window.gui_structure.text_box_multi_line.set_text("Hello")
    assert main_window.gui_structure.text_box_multi_line.label.text() == "Hello"
    main_window.save_scenario()
    assert "text_box_multi_line" in main_window.list_ds[0].to_dict()

    main_window.gui_structure.text_box_multi_line.add_link_2_show(main_window.gui_structure.hint_1, 0)

    with pytest.warns(ConditionalVisibilityWarning):
        main_window.gui_structure.text_box_multi_line.add_link_2_show(main_window.gui_structure.hint_1, 2)

    close_tests(main_window, qtbot)
