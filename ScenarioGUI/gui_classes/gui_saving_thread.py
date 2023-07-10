"""
This document contains all the code related to calculating the solution to the different
aims in the GUI.
"""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable


class SavingThread(QtC.QThread):
    """
    class to calculate the problem in an external thread
    """

    any_signal = QtC.Signal(tuple)

    def __init__(
        self,
        date: datetime.datetime,
        func: Callable[[]],
        parent=None,
    ) -> None:
        """
        This function initialises the calculation class.

        Parameters
        ----------
        date : datetime.datetime
            date of the thread creation time
        func : Callable[[]]
            function for saving
        parent :
            Parent class of the calculation problem
        """
        super().__init__(parent)  # init parent class
        # set datastorage and index
        self.func: Callable = func
        self.date: datetime.datetime = date
        self.calculated: bool = False

    def run(self) -> None:  # pragma: no cover
        """
        This function contains the actual code to run the different calculations.
        For each aim in the GUI, a new if statement is used. Here, one can put all the code
        needed to run the simulation/calculation with the all the functionalities of GHEtool.
        This function should return the DataStorage as a signal.

        Returns
        -------
        None
        """

        try:
            self.func()
        except FileNotFoundError:
            self.calculated = True
            return
        except PermissionError:
            self.calculated = True
            return
        self.calculated = True
