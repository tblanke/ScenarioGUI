from ..starting_closing_tests import close_tests, start_tests


def test_repr(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    assert main_window.gui_structure.category_inputs.__repr__() == "Category; Label: Inputs"
    assert main_window.gui_structure.option_toggle_buttons.__repr__() == "ButtonBox; Label: Use toggle buttons?:, no , yes ; Value: 1"
    assert main_window.gui_structure.hint_1.__repr__() == "Hint; Hint: Grid example; Warning: False"
    assert main_window.gui_structure.float_b.__repr__() == "FloatBox; Label: b; Value: 100.0"
    assert main_window.gui_structure.int_a.__repr__() == "IntBox; Label: a; Value: 2"
    assert main_window.gui_structure.figure_results.__repr__() == "ResultFigure; Label: Plot,X-axis[-],Y-Axis[-]"
    assert main_window.gui_structure.legend_figure_results.__repr__() == "FigureOption; Label: Show legend?; Value: ('legend', False)"
    close_tests(main_window, qtbot)
