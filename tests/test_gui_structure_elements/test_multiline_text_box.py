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

    main_window.gui_structure.text_box_multi_line._init_links()

    assert main_window.gui_structure.text_box_multi_line.get_value() == main_window.gui_structure.text_box_multi_line.default_value
    main_window.gui_structure.text_box_multi_line.set_value("Hello\nWorld")
    assert main_window.gui_structure.text_box_multi_line.get_value() == "Hello\nWorld"

    assert main_window.gui_structure.text_box_multi_line.check_linked_value("Hello\nWorld")

    # test set text
    main_window.gui_structure.text_box_multi_line.set_text("Hello")
    assert main_window.gui_structure.text_box_multi_line.label.text() == "Hello"
    main_window.save_scenario()
    assert "text_box_multi_line" in main_window.list_ds[0].to_dict()
    close_tests(main_window, qtbot)
