import PySide6.QtWidgets as QtW

from ..starting_closing_tests import close_tests, start_tests


def test_category(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    # check if graphics are created
    assert isinstance(main_window.gui_structure.category_grid.graphic_left, QtW.QGraphicsView)
    assert isinstance(main_window.gui_structure.category_grid.graphic_right, QtW.QGraphicsView)
    # check set text
    main_window.gui_structure.category_language.set_text("Hello")
    assert main_window.gui_structure.category_language.label.text() == "Hello"
    main_window.gui_structure.category_language.show()
    assert not main_window.gui_structure.category_language.is_hidden()
    main_window.gui_structure.category_language.hide()
    assert main_window.gui_structure.category_language.is_hidden()
    close_tests(main_window, qtbot)
