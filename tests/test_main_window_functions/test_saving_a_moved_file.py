import os
from pathlib import Path
from sys import setrecursionlimit

from ..starting_closing_tests import close_tests, start_tests
setrecursionlimit(1500)

import ScenarioGUI.global_settings as global_vars

def test_saving_a_moved_fie(qtbot):
    main_window = start_tests(qtbot)
    main_window._save_to_data(f'tests/temp.{global_vars.FILE_EXTENSION}')
    close_tests(main_window, qtbot)
    os.replace(f'tests/temp.{global_vars.FILE_EXTENSION}', f'tests/temp2.{global_vars.FILE_EXTENSION}')
    main_window = start_tests(qtbot)
    main_window.filename = (f'tests/temp2.{global_vars.FILE_EXTENSION}', 0)
    main_window.fun_load_known_filename()
    main_window.fun_save()
    close_tests(main_window, qtbot)
    assert not os.path.exists(f'tests/temp.{global_vars.FILE_EXTENSION}')
    assert os.path.exists(f'tests/temp2.{global_vars.FILE_EXTENSION}')
