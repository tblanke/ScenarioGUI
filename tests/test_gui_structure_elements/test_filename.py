import numpy as np
import PySide6.QtWidgets as QtW
from ScenarioGUI.gui_classes.gui_combine_window import MainWindow
from ScenarioGUI.gui_classes.translation_class import Translations
from ..gui_structure_for_tests import GUI
from ..result_creating_class_for_tests import ResultsClass, data_2_results
import ScenarioGUI.global_settings as global_vars

global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results


def test_filename_read(qtbot) -> None:
    """
    test filename reading function

    Parameters
    ----------
    qtbot: qtbot
        qtbot
    """
    return
    # init gui window
    main_window = MainWindow(QtW.QMainWindow(), qtbot, GUI, Translations)
    main_window.save_scenario()
    main_window.gui_structure.option_filename._init_links()
    import pandas as pd

    from GHEtool import FOLDER
    file = f'{FOLDER.joinpath("Examples/hourly_profile.csv")}'
    # check if no file is passed
    QtC.QTimer.singleShot(1000, lambda: keyboard.press('Esc'))
    main_window.gui_structure.option_filename.button.click()
    assert main_window.gui_structure.option_filename.status_bar.currentMessage() == main_window.gui_structure.option_filename.error_text
    # check file import and calculation
    QtC.QTimer.singleShot(1000, lambda: keyboard.write(file))
    QtC.QTimer.singleShot(1500, lambda: keyboard.press('enter'))
    main_window.gui_structure.option_filename.button.click()
    assert main_window.gui_structure.option_filename.get_value() == file.replace('\\', '/')
    assert main_window.gui_structure.option_filename.check_linked_value(file.replace('\\', '/'))
    main_window.gui_structure.option_column.set_value(1)
    main_window.gui_structure.option_heating_column.set_value(0)
    main_window.gui_structure.option_cooling_column.set_value(1)
    main_window.gui_structure.button_load_csv.button.click()
    main_window.save_scenario()
    borefield, _ = data_2_borefield(main_window.list_ds[-1])
    # check that the borefield baseload is different from main class base load
    g_s = main_window.gui_structure
    borefield_new = create_borefield(g_s)
    borefield_new.load_hourly_profile(file)
    borefield_new.calculate_monthly_load()
    assert not np.allclose(borefield_new.baseload_cooling, borefield.baseload_cooling)
    assert not np.allclose(borefield_new.baseload_heating, borefield.baseload_heating)
    # manually read and calculate load
    d_f = pd.read_csv(file, sep=';', decimal='.')
    heat = d_f[d_f.columns[0]].to_numpy()
    cool = d_f[d_f.columns[1]].to_numpy()
    idx = np.array([0, 31,28,31,30,31,30,31,31,30,31,30,31]).cumsum() * 24
    baseload_heating = [np.sum(heat[idx[i]:idx[i+1]]).astype(np.int64) for i in range(12)]
    baseload_cooling = [np.sum(cool[idx[i]:idx[i+1]]).astype(np.int64) for i in range(12)]
    peak_heating = [np.max(heat[idx[i]:idx[i+1]]).astype(np.int64) for i in range(12)]
    peak_cooling = [np.max(cool[idx[i]:idx[i+1]]).astype(np.int64) for i in range(12)]
    assert np.allclose(baseload_heating, borefield.baseload_heating, atol=1)
    assert np.allclose(baseload_cooling, borefield.baseload_cooling, atol=1)
    assert np.allclose(peak_heating, borefield.peak_heating, atol=1)
    assert np.allclose(peak_cooling, borefield.peak_cooling, atol=1)
    main_window.delete_backup()