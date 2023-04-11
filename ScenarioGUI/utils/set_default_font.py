from __future__ import annotations

import ScenarioGUI.global_settings as globs

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import PySide6.QtWidgets as QtW
    import PySide6.QtGui as QtG


def set_default_font(widget: QtW.QWidget | QtG.QAction, *, bold: bool = False, add_2_size: int = 0) -> None:
    """
    change the font size of the widget

    Parameters
    ----------
    widget: QtW.QWidget
        widget to change the size for

    bold: bool
        should the font be bold?

    add_2_size: int
        point which should be added to the default font size

    Returns
    -------
        None
    """
    font = widget.font()
    font.setFamily(globs.FONT)
    font.setPointSize(globs.FONT_SIZE + add_2_size)
    if bold:
        font.setBold(True)
    widget.setFont(font)
