"""
This document contains all the code related to calculating the solution to the different
aims in the GUI.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import PySide6.QtCore as QtC

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable
    from functools import partial

    import PySide6.QtWidgets as QtW

    from .gui_data_storage import DataStorage


class CalcProblem(QtC.QThread):
    """
    class to calculate the problem in an external thread
    """

    any_signal = QtC.Signal(tuple)
    role: int = 1

    def __init__(
        self,
        d_s: DataStorage,
        item: QtW.QListWidgetItem,
        parent=None,
        *,
        data_2_results_function: Callable[
            [DataStorage],
            tuple[object, partial[[], None]] | tuple[object, Callable[[], None]],
        ],
    ) -> None:
        """
        This function initialises the calculation class.

        Parameters
        ----------
        d_s : DataStorage
            DataStorage object with all the date to perform the calculation for
        idx : int
            Index of the current calculation thread
        parent :
            Parent class of the calculation problem
        data_2_results_function : Callable
            function to create the results class and a function to be called in the thread
        """
        super().__init__(parent)  # init parent class
        # set datastorage and index
        self.d_s = d_s
        self.item = item
        self.data_2_results_function = data_2_results_function
        self.calculated = False

    def run(self) -> None:
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
            results, func = self.data_2_results_function(self.d_s)
            func()
        except Exception as err:
            self.d_s.debug_message = err
            # save bore field in Datastorage
            self.d_s.results = None
            self.calculated = True
            # return Datastorage as signal
            self.item.setData(CalcProblem.role, self.d_s)
            self.any_signal.emit(self)
            return

        # set debug message to ""
        self.d_s.debug_message = ""

        # save borefield in Datastorage
        self.d_s.results = results
        self.calculated = True
        self.item.setData(CalcProblem.role, self.d_s)
        # return Datastorage as signal
        self.any_signal.emit(self)
        return
