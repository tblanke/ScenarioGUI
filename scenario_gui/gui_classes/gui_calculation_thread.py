"""
This document contains all the code related to calculating the solution to the different
aims in the GUI.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import PySide6.QtCore as QtC
from ..global_settings import DATA_2_RESULTS_FUNCTION

if TYPE_CHECKING:  # pragma: no cover
    from .gui_data_storage import DataStorage


class CalcProblem(QtC.QThread):
    """
    class to calculate the problem in an external thread
    """

    any_signal = QtC.Signal(tuple)

    def __init__(self, ds: DataStorage, idx: int, parent=None) -> None:
        """
        This function initialises the calculation class.

        Parameters
        ----------
        ds : DataStorage
            DataStorage object with all the date to perform the calculation for
        idx : int
            Index of the current calculation thread
        parent :
            Parent class of the calculation problem
        """
        super(CalcProblem, self).__init__(parent)  # init parent class
        # set datastorage and index
        self.ds = ds
        self.idx = idx

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

        results, func = DATA_2_RESULTS_FUNCTION(self.ds)

        try:
            func()
        except ValueError as err:
            self.ds.debug_message = err
            # save bore field in Datastorage
            self.ds.results = None
            # return Datastorage as signal
            self.any_signal.emit((self.ds, self.idx))
            return

        # set debug message to ""
        self.ds.debug_message = ""

        # save borefield in Datastorage
        self.ds.results = results
        # return Datastorage as signal
        self.any_signal.emit((self.ds, self.idx))
        return
