"""
script which contain basic gui structure functions
"""
from __future__ import annotations

from typing import Callable, TYPE_CHECKING
from functools import partial as ft_partial

if TYPE_CHECKING:
    import PySide6.QtWidgets as QtW  # type: ignore

    from ScenarioGUI.gui_classes.gui_structure_classes.aim import Aim
    from ScenarioGUI.gui_classes.gui_structure_classes.option import Option


def check_and_set_max_min_values(widget: QtW.QSpinBox | QtW.QDoubleSpinBox, value: int | float, default_max: int | float, default_min: int | float) -> None:
    """
    checks if the value is above the current widget limits but within the default limits:

    Parameters
    ----------
    widget: QtW.QSpinBox | QtW.QDoubleSpinBox
        widget to be checked
    value: int | float
        value to be checked
    default_max: int | float
        default maximal value
    default_min: int | float
        default minimal value

    Returns
    -------
        None
    """
    if default_max > value > widget.maximum():
        widget.setMaximum(default_max)
    if widget.minimum() > value > default_min:
        widget.setMinimum(default_min)


def update_opponent_not_change(button: QtW.QPushButton, false_button_list: list[QtW.QPushButton] = None):
    """
    This function controls the behaviour of the buttons.
    This function makes sure that whenever a button is active, all other buttons except the current one,
    are inactive. If the current button is already active, nothing changes.

    Parameters
    ----------
    button : QtW.QPushButton
        Button which is activated (or pressed on)
    false_button_list : List[QtW.QPushButton]
        List with other buttons which aren't active

    Returns
    -------
    None
    """
    if not button.isChecked():
        button.setChecked(True)
        return
    for but in false_button_list:
        if but != button:
            but.setChecked(False)


def update_opponent_toggle(
    button: QtW.QPushButton,
    button_opponent: QtW.QPushButton,
    false_button_list: list[QtW.QPushButton],
):
    """
    This function controls the behaviour of the buttons, specifically the toggle behaviour.
    This function makes sure that whenever a button is pressed, all other buttons except the current one,
    are inactive. If the current button is already active and it is still pressed, the current button
    is turned inactive and the button_opponent is made active.

    Parameters
    ----------
    button : QtW.QPushButton
        Button which is activated (iff it was not already), and which is deactivated if it was active and is pressed on
    button_opponent : QtW.QPushButton
        Button which is activated if the current button was active and is pressed on
    false_button_list : List[QtW.QPushButton]
        List with other buttons which aren't active

    Returns
    -------
    None
    """
    if button_opponent.isEnabled():
        button_opponent.setChecked(not button.isChecked())
        for false_button in false_button_list:
            false_button.setChecked(False)
        return
    buttons = [button for button in false_button_list if button.isEnabled()]
    if buttons:
        buttons[0].setChecked(not button.isChecked())
        for false_button in buttons[1:]:
            false_button.setChecked(False)
        return
    if not button.isChecked():
        button.setChecked(True)


def check(
    linked_options: list[(Option | list[Option], int)],
    option_input: Option,
    index: int,
    *args,
):
    """
    This function makes sure that the linked_options will be hidden when the index of the option_input
    is different from the index provided per Option in the linked_options list.
    When it is equal, the linked_option is shown.

    Parameters
    ----------
    linked_options : List[(Options, int) or  (List[Options], int)]
        List with linked option, composed of either an Option-index pair or a list of options-index pair
    option_input : Option
        The option which determines the visibility of the linked_options
    index : int
        The index which determines the visibility of the linked_options

    Returns
    -------
    None
    """
    if isinstance(option_input.get_value(), tuple):
        index = index if option_input.get_value()[0] == index else option_input.get_value()[0]
    else:
        index = index if option_input.get_value() == index else option_input.get_value()
    list_false = [(option, idx) for option, idx in linked_options if idx != index]
    list_true = [(option, idx) for option, idx in linked_options if idx == index]
    for option, _ in list_false:
        option.hide()
    for option, _ in list_true:
        option.show()


def check_aim_options(list_aim: list[Aim], *args) -> None:
    """
    This function makes sure that all the options, that are linked to the Aim, are made invisible
    when the aim is not selected and that the options, linked to the Aim, will be shown whenever this Aim
    is selected.

    Parameters
    ----------
    list_aim : List[Aim]
        List with all the aims in the GUI

    Returns
    -------
    None
    """
    list_false = [aim for aim in list_aim if not aim.widget.isChecked()]
    list_true = [aim for aim in list_aim if aim.widget.isChecked()]
    # hide all the options related to the not-checked aims
    for aim in list_false:
        for option in aim.list_options:
            option.hide()
    # show all the options related to the checked aims
    for aim in list_true:
        for option in aim.list_options:
            option.show()


def _create_function_2_check_linked_value(
    option: Option,
    value: int | tuple[int | None, int | None] | tuple[float | None, float | None] | str | bool,
    value_if_hidden: bool | None,
) -> Callable[[], bool]:
    value_if_hidden = option.value_if_hidden if value_if_hidden is None else value_if_hidden
    if value_if_hidden is None:
        return ft_partial(option.check_linked_value, value)

    def func():
        if option.is_hidden():
            return value_if_hidden
        return option.check_linked_value(value)

    return func
