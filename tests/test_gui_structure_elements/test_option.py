from ..starting_closing_tests import close_tests, start_tests


def test_option_functions(qtbot):
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
    float_b.set_tool_tip("Hello World")

    assert float_b.frame.toolTip() == "Hello World"

    assert main_window.gui_structure.int_a.frame.toolTip() == ""

    float_b.label_text = ["b", "b"]

    float_b.set_tool_tip(main_window.translations.float_b_tooltip)

    assert float_b.frame.toolTip() == "This is an explanation\nfor the value b"

    float_b.translate(1)

    assert float_b.frame.toolTip() == "Dies ist eine Erklärung\nfür den Wert b"

    close_tests(main_window, qtbot)
