from tests.starting_closing_tests import close_tests, start_tests


def test_list_box(qtbot):
    # init gui window
    main_window = start_tests(qtbot)

    main_window.gui_structure.float_a.add_link_2_show(main_window.gui_structure.sub_category, 0, 200)
    close_tests(main_window, qtbot)


