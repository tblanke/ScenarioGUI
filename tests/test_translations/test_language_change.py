from ..starting_closing_tests import close_tests, start_tests


def test_language(qtbot):
    """
    test if the language is changed correctly

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    main_window = start_tests(qtbot)

    for idx, action in enumerate(main_window.menu_language.actions()):
        action.trigger()
        assert main_window.gui_structure.option_language.get_value()[0] == idx

    main_window.menu_language.actions()[0].trigger()
    close_tests(main_window, qtbot)
