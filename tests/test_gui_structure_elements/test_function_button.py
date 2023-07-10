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
    assert main_window.res == 5
    # test set text
    main_window.gui_structure.function_button.set_text("Hello")
    assert main_window.gui_structure.function_button.button.text() == "Hello"
    # check show and hide function
    main_window.gui_structure.function_button.show()
    assert not main_window.gui_structure.function_button.is_hidden()
    main_window.gui_structure.function_button.hide()
    assert main_window.gui_structure.function_button.is_hidden()
    close_tests(main_window, qtbot)
