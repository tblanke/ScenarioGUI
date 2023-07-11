import numpy as np

from ..starting_closing_tests import close_tests, start_tests


def test_backup(qtbot):
    # init gui window
    main_window = start_tests(qtbot)
    main_window.add_scenario()
    main_window.gui_structure.float_b.set_value(1.1)
    main_window.gui_structure.int_a.set_value(10)
    main_window.save_scenario()
    list_old = main_window.list_ds.copy()
    thread = main_window.saving_threads[0]
    thread.run()
    assert thread.calculated
    main_window.load_backup()
    # check if the imported values are the same
    for ds_old, ds_new in zip(list_old, main_window.list_ds):
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue

    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    assert thread.calculated
    main_window.save_scenario()
    list_old = main_window.list_ds.copy()
    thread = main_window.saving_threads[0]
    thread.run()
    assert thread.calculated
    main_window.load_backup()
    # check if the imported values are the same
    for ds_old, ds_new in zip(list_old, main_window.list_ds):
        for option in ds_new.list_options_aims:
            if isinstance(getattr(ds_old, option), (int, float)):
                assert np.isclose(getattr(ds_old, option), getattr(ds_new, option))
                continue
            if isinstance(getattr(ds_old, option), (str, bool)):
                assert getattr(ds_old, option) == getattr(ds_new, option)
                continue

    close_tests(main_window, qtbot)
