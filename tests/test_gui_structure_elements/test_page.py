import PySide6.QtWidgets as QtW

from tests.starting_closing_tests import close_tests, start_tests


def test_page(qtbot):
    # init gui window
    main_window = start_tests(qtbot)

    main_window.gui_structure.page_result.set_text("button name,Name")
    assert main_window.gui_structure.page_result.button.text() == "button name"
    assert main_window.gui_structure.page_result.label.text() == "Name"

    # test linked function which counts the counter every time button is clicked
    assert main_window.gui_structure.counter == 1
    main_window.gui_structure.page_inputs.button.click()
    assert main_window.gui_structure.counter == 2
    # check that 3 aim are in a row
    scroll_area = next(widget for widget in main_window.gui_structure.page_inputs.page.children() if isinstance(widget, QtW.QScrollArea))
    assert scroll_area.children()[0].children()[0].children()[1].children()[0].rowCount() == 1
    assert scroll_area.children()[0].children()[0].children()[1].children()[0].columnCount() == 4

    assert main_window.gui_structure.page_inputs.next_page == main_window.gui_structure.page_result
    assert main_window.gui_structure.page_result.previous_page == main_window.gui_structure.page_inputs
    assert main_window.gui_structure.page_result.next_page == main_window.gui_structure.page_settings
    assert main_window.gui_structure.page_settings.previous_page is None

    main_window.gui_structure.page_inputs.next_page = None
    main_window.gui_structure.page_result.previous_page = None
    main_window.gui_structure.page_result.next_page = None

    main_window.gui_structure.automatically_create_page_links()

    assert main_window.gui_structure.page_inputs.next_page == main_window.gui_structure.page_result
    assert main_window.gui_structure.page_result.previous_page == main_window.gui_structure.page_inputs
    assert main_window.gui_structure.page_result.next_page == main_window.gui_structure.page_settings
    assert main_window.gui_structure.page_settings.previous_page == main_window.gui_structure.page_result

    close_tests(main_window, qtbot)
