from functools import partial

from ..starting_closing_tests import start_tests


def test_aim(qtbot):
    """
    test float box functions

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    main_window = start_tests(qtbot)
    if not main_window.gui_structure.aim_plot.widget.isChecked():
        main_window.gui_structure.aim_plot.widget.click()

    assert main_window.gui_structure.aim_plot.widget.isChecked()
    main_window.gui_structure.int_a.set_value(201)
    main_window.save_scenario()
    main_window.add_scenario()
    main_window.gui_structure.int_a.set_value(100)
    main_window.gui_structure.aim_sub.widget.click()
    main_window.save_scenario()
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(0))
    main_window.list_widget_scenario.setCurrentItem(main_window.list_widget_scenario.item(1))

    assert main_window.gui_structure.aim_sub.widget.isChecked()

    main_window.save_scenario()
    main_window.gui_structure.aim_sub.widget.click()
    assert main_window.list_widget_scenario.currentItem().text()[-1] == "*"

    a = []

    def func(val: list):
        val.append(1)

    main_window.gui_structure.aim_plot.change_event(partial(func, a), also_on_visibility=True)
    assert not main_window.gui_structure.button_box.is_hidden()
    main_window.gui_structure.aim_plot.add_link_2_show(main_window.gui_structure.button_box)
    main_window.gui_structure.aim_add.widget.click()
    assert main_window.gui_structure.button_box.is_hidden()
    main_window.gui_structure.aim_plot.widget.click()
    assert not main_window.gui_structure.button_box.is_hidden()

    assert not main_window.gui_structure.aim_plot.is_hidden()
    a_before = len(a)
    main_window.gui_structure.aim_plot.hide()
    assert len(a) == a_before + 1
    assert main_window.gui_structure.aim_plot.is_hidden()
    main_window.gui_structure.aim_plot.show()
    assert len(a) == a_before + 2
    assert not main_window.gui_structure.aim_plot.is_hidden()

    main_window.gui_structure.aim_plot.set_text("Hello")
    assert main_window.gui_structure.aim_plot.widget.text() == "Hello"