"""
script for a status bar logger class
"""
from __future__ import annotations

from functools import partial
from logging import Handler
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC
import PySide6.QtWidgets as QtW

import ScenarioGUI.global_settings as globs

if TYPE_CHECKING:
    from logging import LogRecord

    from PySide6.QtWidgets import QWidget


class StatusBar(Handler):
    """
    Class to create a status bar logger. To display messages in the GUI Status Bar
    """

    def __init__(self, parent: QWidget):
        """
        Init status bar.

        Parameters
        ----------
        parent: QtW.QWidget
            parent to create QStatusBar in
        """
        super().__init__()
        self.label: QtW.QLabel = QtW.QLabel(parent)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
        self.level_2_color: dict[str, str] = {
            "DEBUG": f"{globs.WHITE}",
            "INFO": f"{globs.WHITE}",
            "ERROR": "rgb(255,0,0)",
            "CRITICAL": "rgb(255,0,0)",
            "WARNING": f"{globs.WARNING}",
        }

    def hide_text(self, text: str):
        if self.label.text() == text:
            self.label.setText("")

    def emit(self, record: LogRecord) -> None:
        """
        Display record in statusbar.

        Parameters
        ----------
        record: logging.LogRecord
            record to be displayed

        Returns
        -------
        None

        """
        message = self.format(record)
        timer = QtC.QTimer()
        timer.singleShot(10_000, partial(self.hide_text, message))
        self.label.setStyleSheet(f"color: {self.level_2_color[record.levelname]};")
        self.label.setText(message)
