import pytest

import PySide6.QtWidgets as QtW  # type: ignore

from ScenarioGUI.gui_classes.gui_structure_classes.functions import ConditionalVisibilityWarning
from tests.starting_closing_tests import close_tests, start_tests


def test_list_box(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    # test set value
    assert main_window.gui_structure.list_small_2.get_value()[0] == main_window.gui_structure.list_small_2.default_value
    main_window.gui_structure.list_small_2.set_value(main_window.gui_structure.list_small_2.default_value + 1)
    assert main_window.gui_structure.list_small_2.get_value()[0] == main_window.gui_structure.list_small_2.default_value + 1
    main_window.gui_structure.list_small_2.add_link_2_show(main_window.gui_structure.hint_2, on_index=1)
    # test links
    main_window.gui_structure.list_small_2.set_value(0)
    assert main_window.gui_structure.hint_2.is_hidden()
    main_window.gui_structure.list_small_2.set_value(1)
    assert not main_window.gui_structure.hint_2.is_hidden()
    # test set text
    main_window.gui_structure.list_box.set_text("Hello,4,5,6,7")
    assert main_window.gui_structure.list_box.label.text() == "Hello"
    for i, val in zip(range(4), ["4", "5", "6", "7"]):
        assert main_window.gui_structure.list_box.widget.itemText(i) == val

    main_window.gui_structure.list_small_2.set_value(2)
    assert main_window.gui_structure.list_small_2.get_value()[0] == 2
    main_window.gui_structure.list_small_2.set_value((3, "Hi"))
    assert main_window.gui_structure.list_small_2.get_value() == (3, "3")

    assert main_window.gui_structure.list_small_2.get_value() == (3, "3")
    assert main_window.gui_structure.list_small_2.check_linked_value(3)
    assert not main_window.gui_structure.list_small_2.check_linked_value(2)
    assert main_window.gui_structure.list_small_2.create_function_2_check_linked_value(3)() == main_window.gui_structure.list_small_2.check_linked_value(3)
    main_window.save_scenario()
    assert "list_box" in main_window.list_ds[0].to_dict()

    main_window.gui_structure.list_small_2.add_link_2_show(main_window.gui_structure.hint_1, on_index=0)

    with pytest.warns(ConditionalVisibilityWarning):
        main_window.gui_structure.list_small_2.add_link_2_show(main_window.gui_structure.hint_1, on_index=2)

    main_window.gui_structure.list_small_2.make_editable()
    assert main_window.gui_structure.list_small_2.widget.isEditable()
    assert main_window.gui_structure.list_small_2.widget.insertPolicy() == QtW.QComboBox.InsertPolicy.NoInsert

    main_window.gui_structure.list_small_2.make_editable(True)
    assert main_window.gui_structure.list_small_2.widget.isEditable()
    assert main_window.gui_structure.list_small_2.widget.insertPolicy() == QtW.QComboBox.InsertPolicy.InsertAtBottom

    close_tests(main_window, qtbot)
