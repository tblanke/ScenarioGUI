from ..starting_closing_tests import close_tests, start_tests


def test_datastorage(qtbot):
    """
    tests the datastorage
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.save_scenario()
    main_window.add_scenario()
    assert main_window.list_ds[0] != 2  # noqa: PLR2004
    assert main_window.list_ds[0] == main_window.list_ds[1]
    val_old = main_window.list_ds[1].float_b
    main_window.list_ds[1].float_b = 1
    assert main_window.list_ds[1] != main_window.list_ds[0]
    main_window.list_ds[1].float_b = val_old
    assert main_window.list_ds[0] == main_window.list_ds[1]
    main_window.list_ds[1].list_options_aims.append("no_real_option")
    assert main_window.list_ds[1] != main_window.list_ds[0]
    close_tests(main_window, qtbot)
