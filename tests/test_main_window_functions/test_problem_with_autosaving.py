import os
from functools import partial
from pathlib import Path

import numpy as np
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as global_vars

from ..starting_closing_tests import close_tests, start_tests


def test_problem_with_autosaving(qtbot):  # noqa: PLR0915
    # init gui window
    main_window = start_tests(qtbot)
    gs = main_window.gui_structure
    gs.option_auto_saving.set_value(1)
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    gs.page_result.button.click()
    assert gs.result_text_add.label.text() == "Result: 102.0m"
    gs.int_a.set_value(20)
    main_window.start_current_scenario_calculation()
    thread = main_window.threads[-1]
    thread.run()
    gs.page_result.button.click()
    assert gs.result_text_add.label.text() == "Result: 120.0m"
