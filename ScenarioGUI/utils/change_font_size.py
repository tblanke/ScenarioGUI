from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import PySide6.QtGui as QtG
    import PySide6.QtWidgets as QtW


def change_font_size(widget: QtW.QWidget, size: int, scale_min_height: bool = False) -> None:
    """
    change the font size of the widget

    Parameters
    ----------
    widget: QtW.QWidget
        widget to change the size for
    size: int
        new font size in points

    scale_min_height: bool
        scale the min height together with size

    Returns
    -------
        None
    """
    font = widget.font()
    size_before = font.pointSize()
    font.setPointSize(size)
    widget.setFont(font)
    if scale_min_height:
        min_height = widget.minimumHeight()
        min_height = int(min_height * size / size_before)
        widget.setMinimumHeight(min_height)
